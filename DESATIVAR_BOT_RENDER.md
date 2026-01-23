# 🛑 Desativar Bot no Render (Manter Backend/Frontend Ativos)

## 🎯 Objetivo

Desativar **apenas o bot** no Render, mantendo:
- ✅ **Backend** (`os-sistema-api`) - **ATIVO**
- ✅ **Frontend** (servido pelo backend) - **ATIVO**
- ❌ **Bot** (`os-sistema-bot`) - **DESATIVADO**

---

## 📋 Passo a Passo

### **1. Acessar o Render Dashboard**

1. Abra o navegador
2. Acesse: **https://dashboard.render.com**
3. Faça login com suas credenciais

---

### **2. Encontrar o Serviço do Bot**

1. No dashboard, procure pelo serviço: **`os-sistema-bot`**
2. Clique no nome do serviço para abrir os detalhes

---

### **3. Suspender o Bot**

Você tem **duas opções**:

#### **Opção A: Manual Suspend** (Recomendado - Pode reativar facilmente)

1. No menu lateral do serviço `os-sistema-bot`, procure por **"Manual Suspend"**
2. Clique em **"Suspend"** ou **"Pause"**
3. Confirme a ação
4. O status do serviço mudará para **"Suspended"** ou **"Paused"**

**✅ Vantagem**: Pode reativar facilmente depois clicando em **"Resume"**

---

#### **Opção B: Deletar o Serviço** (Permanente)

⚠️ **CUIDADO**: Esta opção remove o serviço completamente!

1. No menu lateral, vá em **"Settings"**
2. Role até o final da página
3. Clique em **"Delete Service"**
4. Digite o nome do serviço para confirmar
5. Clique em **"Delete"**

**⚠️ Desvantagem**: Se quiser reativar depois, precisará criar o serviço novamente

---

### **4. Verificar Status**

Após suspender/deletar:

1. Volte para o dashboard principal
2. Verifique que:
   - ✅ `os-sistema-api` (Backend) - **Status: Live** ou **Running**
   - ❌ `os-sistema-bot` (Bot) - **Status: Suspended** ou **Deleted**

---

### **5. Testar o Bot Local**

Agora você pode iniciar o bot localmente sem conflito:

1. Execute: **`INICIAR_BOT_LOCAL.bat`**
2. O bot deve iniciar sem erros
3. Teste enviando `/start` no Telegram

---

## ✅ Checklist

- [ ] Acessei o Render Dashboard
- [ ] Encontrei o serviço `os-sistema-bot`
- [ ] Suspendi ou deletei o serviço do bot
- [ ] Verifiquei que `os-sistema-api` continua ativo
- [ ] Testei o bot local (`INICIAR_BOT_LOCAL.bat`)
- [ ] Bot local está funcionando sem conflitos

---

## 🔄 Reativar o Bot no Render (Futuro)

Se você suspendeu (não deletou), para reativar:

1. Acesse o Render Dashboard
2. Encontre o serviço `os-sistema-bot` (status: Suspended)
3. Clique em **"Resume"** ou **"Unpause"**
4. Aguarde alguns segundos
5. O bot voltará a funcionar no Render

**⚠️ Lembre-se**: Se reativar o bot no Render, **pare o bot local** para evitar conflito!

---

## 📝 Notas Importantes

- ✅ **Backend e Frontend continuam funcionando normalmente** no Render
- ✅ **O bot local** vai conectar ao backend do Render (se configurado)
- ✅ **Usuários podem acessar o site** normalmente
- ❌ **O bot no Render não vai responder** enquanto estiver suspenso

---

## 🆘 Problemas?

### **Não encontro o serviço `os-sistema-bot`**
- Verifique se está na organização/conta correta
- Procure na lista de todos os serviços

### **Não vejo a opção "Suspend"**
- Alguns planos do Render podem ter opções diferentes
- Tente procurar por "Pause" ou "Stop"
- Ou use a opção de deletar (se não precisar reativar)

### **Bot local ainda dá erro de conflito**
- Aguarde 1-2 minutos após suspender no Render
- Verifique se não há outros processos Python rodando: `VERIFICAR_BOT_LOCAL.bat`
- Pare processos Python: `taskkill /F /IM python.exe`

---

**Última atualização**: Janeiro 2026
