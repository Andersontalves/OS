"""
Bot Telegram para abertura de Ordens de Serviço

Fluxo de conversação:
1. Foto do power meter
2. Foto da caixa
3. Localização GPS
4. Print da O.S do cliente
5. PPPOE do cliente
6. Confirmação e envio
"""
import logging
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
from services import upload_photo_to_cloudinary, create_os_via_api

# Enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Conversation states
(
    POWER_METER,
    CAIXA,
    LOCALIZACAO,
    PRINT_OS,
    PPPOE,
    CONFIRMACAO
) = range(6)

# User data for each technician (temporary storage)
TECNICO_ID_DEFAULT = 1  # Usar admin (ID 1) para testes se campo1 não existir



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
        "2. Siga as instruções enviando as fotos solicitadas.\n"
        "3. Se precisar parar, clique em *Cancelar Operação*.\n\n"
        "⚠️ *Regras:*\n"
        "• Power meter: máx -21.00 dBm\n"
        "• Localização: precisão < 5m",
        parse_mode="Markdown",
        reply_markup=get_main_menu_keyboard()
    )


async def abrir_os(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Start the OS opening conversation"""
    context.user_data.clear()  # Reset user data
    
    # Create keyboard with location button
    location_keyboard = ReplyKeyboardMarkup(
        [[KeyboardButton("📍 Enviar Localização", request_location=True)],
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

# ... (middle parts unchanged, need to ensure they don't break flow) ...
# Actually, if I change 'abrir_os', I need to check if existing handlers like 'abrir_os' were modified correctly.
# I am replacing start, help, abrir_os.

# I will also modify 'cancel' inside the file separately or include it here if range covers it.
# The user wants "cancelar" button.
# If I use 'confirmation' handler, I should restore main menu.

# Let's use multi_replace or careful replace.
# I'll replace from 'async def start' down to 'async def abrir_os'.

# And I need to update 'main()' to include regex handlers.

# Let's do it in chunks.


async def receive_power_meter(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Receive and process power meter photo"""
    if not update.message.photo:
        await update.message.reply_text(
            "❌ Por favor, envie uma *foto* do power meter.",
            parse_mode="Markdown"
        )
        return POWER_METER
    
    # Get the highest resolution photo
    photo = update.message.photo[-1]
    
    try:
        # Download photo
        photo_file = await context.bot.get_file(photo.file_id)
        photo_bytes = await photo_file.download_as_bytearray()
        
        # Upload to Cloudinary
        await update.message.reply_text("📤 Fazendo upload da foto...")
        photo_url = upload_photo_to_cloudinary(
            photo_bytes,
            filename=f"power_meter_{update.effective_user.id}"
        )
        
        # Store URL
        context.user_data["foto_power_meter"] = photo_url
        
        await update.message.reply_text(
            "✅ Foto do power meter recebida!\n\n"
            "3️⃣ Agora envie a foto da *CAIXA* (mesmo sem adesivo).",
            parse_mode="Markdown"
        )
        
        return CAIXA
    
    except Exception as e:
        logger.error(f"Error uploading power meter photo: {e}")
        await update.message.reply_text(
            f"❌ Erro ao processar foto: {str(e)}\n\n"
            "Por favor, tente novamente."
        )
        return POWER_METER


async def receive_caixa(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Receive and process box photo"""
    if not update.message.photo:
        await update.message.reply_text(
            "❌ Por favor, envie uma *foto* da caixa.",
            parse_mode="Markdown"
        )
        return CAIXA
    
    photo = update.message.photo[-1]
    
    try:
        photo_file = await context.bot.get_file(photo.file_id)
        photo_bytes = await photo_file.download_as_bytearray()
        
        await update.message.reply_text("📤 Fazendo upload da foto...")
        photo_url = upload_photo_to_cloudinary(
            photo_bytes,
            filename=f"caixa_{update.effective_user.id}"
        )
        
        context.user_data["foto_caixa"] = photo_url
        
        await update.message.reply_text(
            "✅ Foto da caixa recebida!\n\n"
            "4️⃣ Envie o *PRINT da O.S* com nome e endereço do cliente.",
            parse_mode="Markdown"
        )
        
        return PRINT_OS
    
    except Exception as e:
        logger.error(f"Error uploading caixa photo: {e}")
        await update.message.reply_text(
            f"❌ Erro ao processar foto: {str(e)}\n\n"
            "Por favor, tente novamente."
        )
        return CAIXA


async def receive_location(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Receive and validate GPS location"""
    if not update.message.location:
        await update.message.reply_text(
            "❌ Por favor, envie sua *localização*.",
            parse_mode="Markdown"
        )
        return LOCALIZACAO
    
    location = update.message.location
    
    # Check horizontal accuracy (if available)
    accuracy = getattr(location, 'horizontal_accuracy', None)
    
    if accuracy and accuracy > config.MAX_LOCATION_PRECISION_METERS:
        await update.message.reply_text(
            f"⚠️ *Precisão atual: {accuracy:.1f} metros*\n\n"
            f"A precisão deve ser *inferior a {config.MAX_LOCATION_PRECISION_METERS} metros*.\n\n"
            "💡 *Dica:* Fique em área aberta e aguarde o GPS calibrar.\n\n"
            "Por favor, envie a localização novamente.",
            parse_mode="Markdown"
        )
        return LOCALIZACAO
    
    # Store location
    context.user_data["localizacao_lat"] = location.latitude
    context.user_data["localizacao_lng"] = location.longitude
    context.user_data["localizacao_precisao"] = accuracy if accuracy else 0
    
    precision_text = f"{accuracy:.1f}m" if accuracy else "N/A"
    
    # Cancel keyboard for during flow
    cancel_kb = ReplyKeyboardMarkup(
        [[KeyboardButton("❌ Cancelar Operação")]], 
        resize_keyboard=True,
        one_time_keyboard=False
    )

    await update.message.reply_text(
        f"✅ Localização confirmada! Precisão: *{precision_text}*\n\n"
        "2️⃣ Agora envie a foto do *POWER METER* com o sinal visível.\n\n"
        "⚠️ O valor *NÃO pode estar acima de -21.00 dBm*.",
        reply_markup=cancel_kb,
        parse_mode="Markdown"
    )
    
    return POWER_METER


async def receive_print_os(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Receive and process client OS print"""
    if not update.message.photo:
        await update.message.reply_text(
            "❌ Por favor, envie uma *foto* do print da O.S.",
            parse_mode="Markdown"
        )
        return PRINT_OS
    
    photo = update.message.photo[-1]
    
    try:
        photo_file = await context.bot.get_file(photo.file_id)
        photo_bytes = await photo_file.download_as_bytearray()
        
        await update.message.reply_text("📤 Fazendo upload da foto...")
        photo_url = upload_photo_to_cloudinary(
            photo_bytes,
            filename=f"print_os_{update.effective_user.id}"
        )
        
        context.user_data["print_os_cliente"] = photo_url
        
        await update.message.reply_text(
            "✅ Print da O.S recebido!\n\n"
            "5️⃣ Por último, *digite o PPPOE do cliente*:",
            parse_mode="Markdown"
        )
        
        return PPPOE
    
    except Exception as e:
        logger.error(f"Error uploading print OS photo: {e}")
        await update.message.reply_text(
            f"❌ Erro ao processar foto: {str(e)}\n\n"
            "Por favor, tente novamente."
        )
        return PRINT_OS


async def receive_pppoe(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Receive PPPOE and show confirmation"""
    if not update.message.text:
        await update.message.reply_text(
            "❌ Por favor, *digite* o PPPOE do cliente.",
            parse_mode="Markdown"
        )
        return PPPOE
    
    pppoe = update.message.text.strip()
    context.user_data["pppoe_cliente"] = pppoe
    
    # Show summary
    summary = (
        "📝 *Resumo da O.S:*\n\n"
        "✓ Foto power meter\n"
        "✓ Foto caixa\n"
        f"✓ Localização ({context.user_data.get('localizacao_precisao', 0):.1f}m precisão)\n"
        "✓ Print O.S cliente\n"
        f"✓ PPPOE: `{pppoe}`\n\n"
        "*Confirmar abertura?*"
    )
    
    keyboard = ReplyKeyboardMarkup(
        [["✅ Sim, confirmar"], ["❌ Cancelar"]],
        one_time_keyboard=True,
        resize_keyboard=True
    )
    
    await update.message.reply_text(
        summary,
        reply_markup=keyboard,
        parse_mode="Markdown"
    )
    
    return CONFIRMACAO


async def confirmation(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle confirmation and create OS via API"""
    response = update.message.text.strip()
    
    if "Sim" in response or "confirmar" in response.lower():
        await update.message.reply_text(
            "📤 Enviando O.S para o sistema...",
            reply_markup=ReplyKeyboardRemove()
        )
        
        try:
            # Prepare data for API
            os_data = {
                "tipo_servico": "INSTALACAO",
                "descricao": "Abertura via Bot Telegram",
                "prioridade": "NORMAL",
                "tecnico_campo_id": TECNICO_ID_DEFAULT,
                "foto_power_meter": context.user_data["foto_power_meter"],
                "foto_caixa": context.user_data["foto_caixa"],
                "localizacao_lat": context.user_data["localizacao_lat"],
                "localizacao_lng": context.user_data["localizacao_lng"],
                "localizacao_precisao": context.user_data.get("localizacao_precisao"),
                "print_os_cliente": context.user_data["print_os_cliente"],
                "pppoe_cliente": context.user_data["pppoe_cliente"]
            }
            
            # Create OS via API
            result = create_os_via_api(os_data)
            
            await update.message.reply_text(
                "✅ *O.S criada com sucesso!*\n\n"
                f"📋 Número: *{result['numero_os']}*\n"
                f"⏰ Criada em: {result['criado_em'][:16]}\n"
                f"📊 Status: *{result['status']}*\n\n"
                "Aguardando atribuição pela equipe de execução.\n\n"
                "Aguardando atribuição pela equipe de execução.\n\n"
                "Selecione uma opção:",
                parse_mode="Markdown",
                reply_markup=get_main_menu_keyboard()
            )
            
            context.user_data.clear()
            return ConversationHandler.END
        
        except Exception as e:
            logger.error(f"Error creating OS: {e}")
            await update.message.reply_text(
                f"❌ Erro ao criar O.S:\n\n{str(e)}\n\nPor favor, tente novamente com /abrir_os",
                parse_mode=None
            )
            context.user_data.clear()
            return ConversationHandler.END
    
    else:
        await update.message.reply_text(
            "❌ Abertura de O.S cancelada.\n\n"
            "❌ Abertura de O.S cancelada.\n\n"
            "Selecione uma opção:",
            reply_markup=get_main_menu_keyboard()
        )
        context.user_data.clear()
        return ConversationHandler.END


async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Cancel the conversation"""
    await update.message.reply_text(
        "❌ Operação cancelada.\n\n"
        "Selecione uma opção:",
        reply_markup=get_main_menu_keyboard()
    )
    context.user_data.clear()
    return ConversationHandler.END


def main():
    """Start the bot"""
    if not config.TELEGRAM_BOT_TOKEN:
        logger.error("❌ TELEGRAM_BOT_TOKEN não configurado no .env!")
        return
    
    # Create application
    application = Application.builder().token(config.TELEGRAM_BOT_TOKEN).build()
    
    # Conversation handler for opening OS
    conv_handler = ConversationHandler(
        entry_points=[
            CommandHandler("abrir_os", abrir_os),
            MessageHandler(filters.Regex("^📋 Abrir Nova O.S.$"), abrir_os)
        ],
        states={
            POWER_METER: [MessageHandler(filters.PHOTO, receive_power_meter)],
            CAIXA: [MessageHandler(filters.PHOTO, receive_caixa)],
            LOCALIZACAO: [MessageHandler(filters.LOCATION, receive_location)],
            PRINT_OS: [MessageHandler(filters.PHOTO, receive_print_os)],
            PPPOE: [MessageHandler(filters.TEXT & ~filters.COMMAND, receive_pppoe)],
            CONFIRMACAO: [MessageHandler(filters.TEXT & ~filters.COMMAND, confirmation)],
        },
        fallbacks=[
            CommandHandler("cancelar", cancel),
            MessageHandler(filters.Regex("^❌ Cancelar Operação$"), cancel)
        ],
    )
    
    # Add handlers
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(MessageHandler(filters.Regex("^❓ Ajuda$"), help_command))
    application.add_handler(conv_handler)
    
    # Start bot
    logger.info("🤖 Bot iniciando...")
    application.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()
