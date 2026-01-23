# 🔧 Configurar Render API para Reiniciar Bot

## 📋 Como Funciona

Quando você clica em "Destravar Bot" e o bot está offline, o sistema pode **reiniciar automaticamente** o bot via API do Render.

## 🔑 Passo 1: Obter API Key do Render

1. Acesse: https://dashboard.render.com
2. Vá em **Account Settings** (canto superior direito → seu nome)
3. Role até **API Keys**
4. Clique em **"Create API Key"**
5. Dê um nome (ex: "Bot Restart")
6. **Copie o token** (começa com `rnd_...`)
   - ⚠️ **IMPORTANTE**: Só aparece uma vez! Salve bem.

## 🆔 Passo 2: Obter Service ID do Bot

1. No Render Dashboard, vá no serviço **`os-sistema-bot`**
2. Vá em **Settings**
3. Role até encontrar **"Service ID"**
4. **Copie o ID** (formato: `srv_xxxxxxxxxxxxx`)
   - Ou pegue da URL: `https://dashboard.render.com/web/srv_xxxxxxxxxxxxx`

## ⚙️ Passo 3: Configurar no Render

No serviço **`os-sistema-api`** (backend):

1. Vá em **Environment** (Environment Variables)
2. Adicione duas variáveis:

   **Variável 1:**
   - **Nome:** `RENDER_API_KEY`
   - **Valor:** `rnd_xxxxxxxxxxxxx` (o token que você copiou)

   **Variável 2:**
   - **Nome:** `RENDER_BOT_SERVICE_ID`
   - **Valor:** `srv_xxxxxxxxxxxxx` (o Service ID do bot)

3. **Salve** as alterações
4. O serviço vai reiniciar automaticamente

## ✅ Como Testar

1. Aguarde o backend reiniciar (1-2 minutos)
2. Acesse a página de login
3. Clique em **"🔧 Destravar Bot"**
4. Se o bot estiver offline, você verá:
   - `✅ Bot reiniciado via Render API! Aguarde 1-2 minutos para ele voltar online.`

## 🔍 Como o Sistema Detecta Bot Offline

**NÃO consulta o site do Render!** Funciona assim:

1. **Bot faz heartbeat** a cada 8 minutos chamando `/keepalive`
2. **Backend registra** o timestamp em `bot_last_heartbeat`
3. **Quando você clica "Destravar Bot"**:
   - Sistema verifica `bot_last_heartbeat`
   - Calcula: `tempo_atual - bot_last_heartbeat`
   - Se passou mais de 10 minutos → considera offline
4. **Se offline** → chama API do Render para reiniciar

## 💡 Vantagens

- ✅ **Automático**: Não precisa ir no Render manualmente
- ✅ **Rápido**: Reinicia em segundos
- ✅ **Simples**: Só precisa configurar uma vez
- ✅ **Seguro**: Token fica nas variáveis de ambiente

## ⚠️ Importante

- O token da API do Render é **sensível** - não compartilhe
- Se não configurar, o botão ainda funciona, mas não reinicia automaticamente
- O reinício pode demorar 1-2 minutos para o bot voltar online
