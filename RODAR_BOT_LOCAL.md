# 🤖 Rodar Bot Localmente (Mais Simples)

## ✅ Opção Recomendada: Bot Local + Backend/Site no Render

**Vantagens:**
- ✅ Bot roda no seu PC (você controla, reinicia quando quiser)
- ✅ Site/API no Render (acessível de qualquer lugar)
- ✅ Banco Supabase (gratuito, não para)
- ✅ Mais simples de gerenciar

## 📋 Configuração Rápida

### 1. Configurar o Bot para Usar API do Render

No arquivo `telegram-bot/.env`:

```env
TELEGRAM_BOT_TOKEN=seu_token_do_telegram
API_BASE_URL=https://os-sistema-api.onrender.com
CLOUDINARY_URL=sua_url_cloudinary
```

**Importante:** 
- `API_BASE_URL` aponta para o Render (não `localhost`)
- O bot vai se conectar à API no Render
- Você só precisa do PC ligado para o bot funcionar

### 2. Instalar Dependências (se ainda não instalou)

```bash
cd telegram-bot
pip install -r requirements.txt
```

### 3. Rodar o Bot

```bash
cd telegram-bot
python bot.py
```

**Pronto!** O bot vai:
- ✅ Conectar na API do Render
- ✅ Funcionar normalmente
- ✅ Você pode fechar/abrir quando quiser

## 🔄 Reiniciar o Bot

Se o bot travar:
1. Pressione `Ctrl+C` no terminal
2. Execute novamente: `python bot.py`

Ou crie um arquivo `iniciar_bot.bat`:

```batch
@echo off
cd telegram-bot
python bot.py
pause
```

## 🎯 Resumo da Arquitetura

```
┌─────────────────┐
│   Seu PC        │
│                 │
│  ┌───────────┐  │
│  │ Bot Local │──┼──► API no Render
│  └───────────┘  │      (os-sistema-api.onrender.com)
│                 │
└─────────────────┘
         │
         ▼
    Telegram
    (usuários)
```

**Backend/Site:** Render (sempre online)
**Bot:** Seu PC (você controla)
**Banco:** Supabase (gratuito, não para)

## ⚠️ Importante

- O bot precisa do seu PC ligado para funcionar
- Se desligar o PC, o bot para (mas o site continua funcionando)
- Quando ligar de novo, só executar `python bot.py`

## 💡 Dica: Rodar em Background (Opcional)

Se quiser rodar o bot em background no Windows:

1. Crie `iniciar_bot_background.bat`:
```batch
@echo off
cd telegram-bot
start /B python bot.py
echo Bot iniciado em background!
pause
```

2. Para parar, abra o Gerenciador de Tarefas e finalize o processo `python.exe`

## 🆚 Comparação de Opções

| Opção | Bot | Backend | Banco | Complexidade |
|-------|-----|---------|-------|--------------|
| **Tudo Local** | PC | PC | SQLite | ⭐ Muito Simples |
| **Híbrido (Recomendado)** | PC | Render | Supabase | ⭐⭐ Simples |
| **Tudo Nuvem** | Render | Render | Supabase | ⭐⭐⭐ Médio |

## ✅ Próximos Passos

1. ✅ Configure `telegram-bot/.env` com `API_BASE_URL` do Render
2. ✅ Execute `python bot.py`
3. ✅ Teste enviando `/start` no Telegram
4. ✅ Pronto! Bot funcionando localmente

---

**Não precisa mais configurar Render API para reiniciar bot!** 
Você mesmo reinicia quando quiser! 🎉
