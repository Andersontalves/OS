# 🤖 Bot Local - Guia de Uso

## ✅ Configuração Atual

O bot está configurado para rodar **localmente** e **não vai travar** porque:

1. ✅ Usa `.env.local` (bot de teste separado)
2. ✅ Conecta ao backend local (`http://localhost:8000`)
3. ✅ Não depende do Render para funcionar
4. ✅ Roda continuamente enquanto o computador estiver ligado

## 🚀 Como Iniciar o Bot Local

### Opção 1: Script Automático (Recomendado)

Execute:
```
INICIAR_BOT_LOCAL.bat
```

### Opção 2: Manual

```bash
cd telegram-bot
python bot.py
```

## ⚙️ Configuração

O bot local usa o arquivo `telegram-bot/.env.local`:

```env
TELEGRAM_BOT_TOKEN=8558207794:AAFjF-F_bg7pAM1Gw2Vn0R2k2VLycBXlIgo
API_BASE_URL=http://localhost:8000
CLOUDINARY_URL=cloudinary://api_key:api_secret@cloud_name
```

## 📋 Requisitos

Para o bot funcionar localmente, você precisa:

1. ✅ **Backend rodando localmente** na porta 8000
   - Execute: `INICIAR_BACKEND.bat`
   - Ou: `cd backend && python -m uvicorn app.main:app --reload --port 8000`

2. ✅ **Arquivo `.env.local` configurado** no `telegram-bot/`

3. ✅ **Python e dependências instaladas**

## 🔄 Diferença: Bot Local vs Bot no Render

| Aspecto | Bot Local | Bot no Render |
|---------|-----------|---------------|
| **Onde roda** | Seu computador | Servidor Render |
| **Trava?** | ❌ Não (enquanto PC ligado) | ⚠️ Pode travar após 15min inativo |
| **Token** | Bot de teste (`.env.local`) | Bot de produção (`.env`) |
| **API** | `localhost:8000` | URL do Render |
| **Uso** | Desenvolvimento/Testes | Produção |

## 💡 Dicas

1. **Manter bot rodando**: Deixe a janela do terminal aberta
2. **Reiniciar bot**: Pare (Ctrl+C) e execute `INICIAR_BOT_LOCAL.bat` novamente
3. **Ver logs**: Os logs aparecem na janela do terminal
4. **Backend offline**: Se o backend não estiver rodando, o bot não conseguirá criar O.S

## 🛑 Parar o Bot

Pressione `Ctrl+C` na janela do terminal onde o bot está rodando.

## ✅ Status Atual

- ✅ Bot local configurado
- ✅ Usa bot de teste separado
- ✅ Não interfere com produção
- ✅ Roda continuamente (não trava)

---

**Nota**: O bot de produção no Render continua funcionando normalmente. O bot local é apenas para testes/desenvolvimento.
