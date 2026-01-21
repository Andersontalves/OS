# Bot Telegram - Sistema O.S

Bot para técnicos de campo abrirem Ordens de Serviço via Telegram.

## 🚀 Como Obter o Token do Bot

1. Abra o Telegram e procure por `@BotFather`
2. Envie `/newbot`
3. Escolha um nome (ex: "Sistema OS InfraNet")
4. Escolha um username (ex: `infranet_os_bot`)
5. Copie o token fornecido

## ⚙️ Configuração

1. Copie o arquivo de exemplo:
```bash
copy .env.example .env
```

2. Edite `.env` e adicione:
```
TELEGRAM_BOT_TOKEN=seu_token_aqui
API_BASE_URL=http://localhost:8000
CLOUDINARY_URL=seu_cloudinary_url
```

## ▶️ Executar Localmente

```bash
pip install -r requirements.txt
python bot.py
```

## 📱 Como Usar

1. Abra o bot no Telegram
2. `/start` para iniciar
3. `/abrir_os` para abrir uma O.S
4. Siga as instruções:
   - Enviar foto do power meter
   - Enviar foto da caixa
   - Enviar localização GPS
   - Enviar print da O.S do cliente
   - Digitar PPPOE
   - Confirmar

## 🔧 Comandos

- `/start` - Inicializar bot
- `/abrir_os` - Abrir nova O.S
- `/cancelar` - Cancelar abertura
- `/help` - Ajuda

## 🌍 Deploy (Railway)

1. Conecte o repositório no Railway
2. Configure as variáveis de ambiente
3. O bot iniciará automaticamente!

## ⚠️ Validações

- **Power meter**: Sinal não pode estar acima de -21.00 dBm
- **Localização**: Precisão deve ser inferior a 5 metros
- **Fotos**: Formato de imagem válido
