"""
Bot Telegram para abertura de Ordens de Serviço

Fluxo de conversação:
1. Localização GPS
2. Cidade do atendimento
3. Motivo da O.S
4. Foto do power meter
5. Foto da caixa
6. Print da O.S do cliente
7. PPPOE do cliente
8. Confirmação e envio
"""
import logging
import threading
from http.server import BaseHTTPRequestHandler, HTTPServer
import os
from telegram import Update, ReplyKeyboardMarkup, ReplyKeyboardRemove, KeyboardButton
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    ConversationHandler,
    ContextTypes,
    filters,
)
import config
from services import upload_photo_to_cloudinary, create_os_via_api, check_api_health
import time
import asyncio

# Enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Conversation states
(
    LOCALIZACAO,
    CIDADE,
    MOTIVO,
    POWER_METER,
    CAIXA,
    PRINT_OS,
    PPPOE,
    CONFIRMACAO
) = range(8)

# User data default
TECNICO_ID_DEFAULT = 1  # Admin ID

# Menu helpers
def get_main_menu_keyboard():
    return ReplyKeyboardMarkup(
        [
            [KeyboardButton("📋 Abrir Nova O.S.")],
            [KeyboardButton("❓ Ajuda"), KeyboardButton("❌ Cancelar Operação")]
        ],
        resize_keyboard=True
    )

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Start command - welcome message"""
    user = update.effective_user
    await update.message.reply_text(
        f"👋 Olá, {user.first_name}!\n\n"
        "Bem-vindo ao Sistema de Ordens de Serviço.\n"
        "Selecione uma opção no menu abaixo:",
        reply_markup=get_main_menu_keyboard()
    )

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Help command"""
    await update.message.reply_text(
        "📋 *Sistema de Ordens de Serviço - Ajuda*\n\n"
        "*Como usar:*\n"
        "Use os botões do menu para navegar.\n\n"
        "1. Clique em *Abrir Nova O.S.*\n"
        "2. Siga as instruções enviando as informações solicitadas.\n"
        "3. Se precisar parar, clique em *Cancelar Operação*.\n\n"
        "⚠️ *Regras:*\n"
        "• Power meter: máx -21.00 dBm\n"
        "• Localização: precisão < 5m",
        parse_mode="Markdown",
        reply_markup=get_main_menu_keyboard()
    )

async def status_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Diagnostic command to check bot and API status"""
    logger.info(f"🔍 Status solicitado por: {update.effective_user.username}")
    
    start_time = time.time()
    api_status = await check_api_health()
    latency = round((time.time() - start_time) * 1000, 2)
    
    status_msg = (
        "🤖 *Status do Sistema*\n\n"
        f"✅ *Bot:* Ativo e Online\n"
        f"📡 *API:* {'✅ Online' if api_status else '❌ Offline'}\n"
        f"⏱️ *Latência:* {latency}ms\n\n"
        f"🏠 *Ambiente:* Render (Free Tier)\n"
        "> Nota: Se a API estiver offline, ela pode estar acordando (hibernação)."
    )
    
    await update.message.reply_text(status_msg, parse_mode="Markdown")

async def abrir_os(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Start the OS opening process by requesting location"""
    logger.info(f"Bot: Comando 'abrir_os' recebido de {update.effective_user.username}")
    context.user_data.clear()
    
    location_keyboard = ReplyKeyboardMarkup(
        [[KeyboardButton("📍 Enviar Localização (GPS)", request_location=True)],
         [KeyboardButton("❌ Cancelar Operação")]],
        one_time_keyboard=True,
        resize_keyboard=True
    )
    
    await update.message.reply_text(
        "📋 *Vamos abrir uma nova Ordem de Serviço!*\n\n"
        "1️⃣ O primeiro passo é enviar sua *LOCALIZAÇÃO ATUAL*.\n\n"
        "📍 Clique no botão abaixo para compartilhar seu GPS.\n"
        "⚠️ A precisão deve ser *inferior a 5 metros*.",
        parse_mode="Markdown",
        reply_markup=location_keyboard
    )
    return LOCALIZACAO

async def receive_location(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Receive and validate GPS location"""
    if not update.message.location:
        await update.message.reply_text("❌ Por favor, envie sua *localização*.")
        return LOCALIZACAO
    
    location = update.message.location
    accuracy = getattr(location, 'horizontal_accuracy', None)
    
    if accuracy and accuracy > config.MAX_LOCATION_PRECISION_METERS:
        await update.message.reply_text(
            f"⚠️ *Precisão atual: {accuracy:.1f} metros*\n"
            f"A precisão deve ser inferior a {config.MAX_LOCATION_PRECISION_METERS}m.\n"
            "Tente enviar novamente em área aberta.",
            parse_mode="Markdown"
        )
        return LOCALIZACAO
    
    context.user_data["localizacao_lat"] = location.latitude
    context.user_data["localizacao_lng"] = location.longitude
    context.user_data["localizacao_precisao"] = accuracy if accuracy else 0
    
    user = update.effective_user
    context.user_data["telegram_nick"] = f"@{user.username}" if user.username else user.full_name
    
    cidade_keyboard = ReplyKeyboardMarkup(
        [["Salto de Pirapora", "Votorantim"],
         ["Araçoiaba da Serra", "Sarapuí"],
         ["Sorocaba", "Alambarí"],
         ["❌ Cancelar Operação"]],
        one_time_keyboard=True,
        resize_keyboard=True
    )

    await update.message.reply_text(
        "✅ Localização recebida!\n\n"
        "2️⃣ Qual a *CIDADE* do atendimento?",
        parse_mode="Markdown",
        reply_markup=cidade_keyboard
    )
    return CIDADE

async def receive_cidade(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Receive and process the city"""
    cidade = update.message.text
    cidades_validas = ["Salto de Pirapora", "Votorantim", "Araçoiaba da Serra", "Sarapuí", "Sorocaba", "Alambarí"]
    
    if cidade not in cidades_validas:
        await update.message.reply_text("Escolha uma cidade no teclado.")
        return CIDADE
        
    context.user_data["cidade"] = cidade
    
    motivo_keyboard = ReplyKeyboardMarkup(
        [["Caixa sem sinal", "Ampliação de atendimento"],
         ["Sinal Alto", "❌ Cancelar Operação"]],
        one_time_keyboard=True,
        resize_keyboard=True
    )

    await update.message.reply_text(
        f"✅ Cidade: *{cidade}*\n\n"
        "3️⃣ Qual o *MOTIVO* da abertura desta O.S?",
        parse_mode="Markdown",
        reply_markup=motivo_keyboard
    )
    return MOTIVO

async def receive_motivo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Receive and process the reason"""
    motivo = update.message.text
    if motivo not in ["Caixa sem sinal", "Ampliação de atendimento", "Sinal Alto"]:
        await update.message.reply_text("Escolha uma opção no teclado.")
        return MOTIVO
        
    context.user_data["motivo_abertura"] = motivo
    
    cancel_kb = ReplyKeyboardMarkup([[KeyboardButton("❌ Cancelar Operação")]], resize_keyboard=True)

    await update.message.reply_text(
        f"✅ Motivo: *{motivo}*\n\n"
        "4️⃣ Agora envie a foto do *POWER METER*...",
        parse_mode="Markdown",
        reply_markup=cancel_kb
    )
    return POWER_METER

async def receive_power_meter(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Receive and process power meter photo"""
    if not update.message.photo:
        await update.message.reply_text("❌ Envie uma *foto*.", parse_mode="Markdown")
        return POWER_METER
    
    photo = update.message.photo[-1]
    try:
        photo_file = await context.bot.get_file(photo.file_id)
        photo_bytes = await photo_file.download_as_bytearray()
        
        await update.message.reply_text("📤 Fazendo upload...")
        photo_url = upload_photo_to_cloudinary(photo_bytes, filename=f"pm_{update.effective_user.id}")
        context.user_data["foto_power_meter"] = photo_url
        
        await update.message.reply_text(
            "✅ Foto PM recebida!\n\n"
            "5️⃣ Agora envie a foto da *CAIXA*:",
            parse_mode="Markdown"
        )
        return CAIXA
    except Exception as e:
        logger.error(f"Error PM photo: {e}")
        await update.message.reply_text(f"❌ Erro: {str(e)}")
        return POWER_METER

async def receive_caixa(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Receive and process box photo"""
    if not update.message.photo:
        await update.message.reply_text("❌ Envie uma *foto*.", parse_mode="Markdown")
        return CAIXA
    
    photo = update.message.photo[-1]
    try:
        photo_file = await context.bot.get_file(photo.file_id)
        photo_bytes = await photo_file.download_as_bytearray()
        
        await update.message.reply_text("📤 Fazendo upload...")
        photo_url = upload_photo_to_cloudinary(photo_bytes, filename=f"cx_{update.effective_user.id}")
        context.user_data["foto_caixa"] = photo_url
        
        await update.message.reply_text(
            "✅ Foto Caixa recebida!\n\n"
            "6️⃣ Envie o *PRINT da O.S* (nome/end do cliente):",
            parse_mode="Markdown"
        )
        return PRINT_OS
    except Exception as e:
        logger.error(f"Error Caixa photo: {e}")
        await update.message.reply_text(f"❌ Erro: {str(e)}")
        return CAIXA

async def receive_print_os(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Receive and process print OS"""
    if not update.message.photo:
        await update.message.reply_text("❌ Envie uma *foto*.", parse_mode="Markdown")
        return PRINT_OS
    
    photo = update.message.photo[-1]
    try:
        photo_file = await context.bot.get_file(photo.file_id)
        photo_bytes = await photo_file.download_as_bytearray()
        
        await update.message.reply_text("📤 Fazendo upload...")
        photo_url = upload_photo_to_cloudinary(photo_bytes, filename=f"print_{update.effective_user.id}")
        context.user_data["print_os_cliente"] = photo_url
        
        await update.message.reply_text(
            "✅ Print O.S recebido!\n\n"
            "7️⃣ Por último, digite o *PPPOE* do cliente:",
            parse_mode="Markdown"
        )
        return PPPOE
    except Exception as e:
        logger.error(f"Error Print OS: {e}")
        await update.message.reply_text(f"❌ Erro: {str(e)}")
        return PRINT_OS

async def receive_pppoe(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Receive PPPOE and show summary"""
    pppoe = update.message.text.strip()
    context.user_data["pppoe_cliente"] = pppoe
    
    summary = (
        "📝 *Resumo da O.S:*\n"
        f"📍 Cidade: *{context.user_data.get('cidade')}*\n"
        f"💡 Motivo: *{context.user_data.get('motivo_abertura')}*\n"
        f"🔑 PPPOE: `{pppoe}`\n\n"
        "*Confirmar abertura?*"
    )
    
    keyboard = ReplyKeyboardMarkup([["✅ Confirmar"], ["❌ Cancelar Operação"]], one_time_keyboard=True, resize_keyboard=True)
    await update.message.reply_text(summary, reply_markup=keyboard, parse_mode="Markdown")
    return CONFIRMACAO

async def confirmation(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Create OS via API"""
    response = update.message.text.strip()
    if "Confirmar" in response:
        await update.message.reply_text("📤 Enviando O.S...", reply_markup=ReplyKeyboardRemove())
        try:
            os_data = {
                "tecnico_campo_id": TECNICO_ID_DEFAULT,
                "foto_power_meter": context.user_data["foto_power_meter"],
                "foto_caixa": context.user_data["foto_caixa"],
                "localizacao_lat": context.user_data["localizacao_lat"],
                "localizacao_lng": context.user_data["localizacao_lng"],
                "localizacao_precisao": context.user_data.get("localizacao_precisao"),
                "print_os_cliente": context.user_data["print_os_cliente"],
                "pppoe_cliente": context.user_data["pppoe_cliente"],
                "motivo_abertura": context.user_data.get("motivo_abertura"),
                "telegram_nick": context.user_data.get("telegram_nick"),
                "cidade": context.user_data.get("cidade")
            }
            result = await create_os_via_api(os_data)
            await update.message.reply_text(
                f"✅ *O.S criada!* Nº: *{result['numero_os']}*\n"
                "Em breve um técnico assumirá a execução.",
                parse_mode="Markdown",
                reply_markup=get_main_menu_keyboard()
            )
            context.user_data.clear()
            return ConversationHandler.END
        except Exception as e:
            logger.error(f"Error creating OS: {e}")
            await update.message.reply_text(f"❌ Erro ao criar O.S: {str(e)}")
            return ConversationHandler.END
    else:
        await update.message.reply_text("❌ Cancelado.", reply_markup=get_main_menu_keyboard())
        return ConversationHandler.END

async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Cancel conversation"""
    await update.message.reply_text("❌ Operação cancelada.", reply_markup=get_main_menu_keyboard())
    context.user_data.clear()
    return ConversationHandler.END

async def api_heartbeat(context: ContextTypes.DEFAULT_TYPE):
    """Callback for JobQueue to keep API awake"""
    try:
        is_alive = await check_api_health()
        if is_alive:
            logger.debug("💓 API está acordada.")
        else:
            logger.warning("💓 API não respondeu ao heartbeat.")
    except Exception as e:
        logger.error(f"💓 Falha no heartbeat: {e}")

def main():
    """Start the bot"""
    if not config.TELEGRAM_BOT_TOKEN:
        logger.error("❌ TOKEN não configurado!")
        return
    
    application = Application.builder().token(config.TELEGRAM_BOT_TOKEN).build()
    
    conv_handler = ConversationHandler(
        entry_points=[
            CommandHandler("abrir_os", abrir_os),
            MessageHandler(filters.Regex("^📋 Abrir Nova O.S.$"), abrir_os)
        ],
        states={
            LOCALIZACAO: [MessageHandler(filters.LOCATION, receive_location)],
            CIDADE: [MessageHandler(filters.TEXT & ~filters.COMMAND & ~filters.Regex("^❌"), receive_cidade)],
            MOTIVO: [MessageHandler(filters.TEXT & ~filters.COMMAND & ~filters.Regex("^❌"), receive_motivo)],
            POWER_METER: [MessageHandler(filters.PHOTO, receive_power_meter)],
            CAIXA: [MessageHandler(filters.PHOTO, receive_caixa)],
            PRINT_OS: [MessageHandler(filters.PHOTO, receive_print_os)],
            PPPOE: [MessageHandler(filters.TEXT & ~filters.COMMAND & ~filters.Regex("^❌"), receive_pppoe)],
            CONFIRMACAO: [MessageHandler(filters.TEXT & ~filters.COMMAND & ~filters.Regex("^❌"), confirmation)],
        },
        fallbacks=[
            CommandHandler("cancelar", cancel),
            MessageHandler(filters.Regex("^❌ Cancelar Operação$"), cancel)
        ],
    )
    
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler("status", status_command))
    application.add_handler(MessageHandler(filters.Regex("^❓ Ajuda$"), help_command))
    application.add_handler(conv_handler)
    
    # Configure heartbeat every 10 minutes
    if application.job_queue:
        application.job_queue.run_repeating(api_heartbeat, interval=600, first=10)
        logger.info("💓 Heartbeat da API agendado (10min).")
    
    logger.info("🤖 Bot configurado. Iniciando polling...")
    try:
        application.run_polling(allowed_updates=Update.ALL_TYPES, close_loop=False)
    except Exception as e:
        logger.error(f"❌ Erro no polling: {e}")
        raise e

class HealthCheckHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/plain')
        self.end_headers()
        self.wfile.write(b"Bot is alive!")
    def log_message(self, format, *args):
        return

def run_health_check_server():
    try:
        port = int(os.environ.get("PORT", "10000"))
        server = HTTPServer(('0.0.0.0', port), HealthCheckHandler)
        logger.info(f"📡 Servidor Health Check rodando na porta {port}")
        server.serve_forever()
    except Exception as e:
        logger.error(f"⚠️ Erro no servidor de saúde: {e}")

if __name__ == "__main__":
    logger.info("🎬 Iniciando processo principal do Bot...")
    # Health check em thread separada
    threading.Thread(target=run_health_check_server, daemon=True).start()
    
    max_retries = 5
    retry_delay = 10  # seconds
    
    for attempt in range(max_retries):
        try:
            main()
            break # Exit loop if main returns normally
        except KeyboardInterrupt:
            logger.info("🛑 Parado pelo usuário.")
            break
        except Exception as e:
            logger.error(f"💥 Falha no Bot (Tentativa {attempt + 1}/{max_retries}): {e}")
            if attempt < max_retries - 1:
                logger.info(f"⏳ Reiniciando em {retry_delay}s...")
                time.sleep(retry_delay)
            else:
                logger.critical("❌ Limite de tentativas atingido. O bot parou.")
                os._exit(1)
