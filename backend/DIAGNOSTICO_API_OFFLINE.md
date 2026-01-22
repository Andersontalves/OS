# 🔍 Diagnóstico: API Não Responde (Bot Travado)

## ❌ Problema Identificado

O bot está travado porque a **API backend não está respondendo**:
- Logs mostram: `💔 API não respondeu ao heartbeat.`
- O bot para de funcionar quando a API não responde

## 🔍 Possíveis Causas

1. **API hibernada** (Free tier do Render)
   - Render free tier hiberna após 15min de inatividade
   - O keep-alive pode não estar funcionando

2. **API com erro ao iniciar**
   - Erro de conexão com Supabase
   - Erro ao criar tabelas
   - Erro ao criar usuários

3. **API não iniciou**
   - Deploy falhou
   - Variáveis de ambiente incorretas

## ✅ Solução Passo a Passo

### 1. Verificar Status da API no Render

1. Acesse o Render Dashboard
2. Vá no serviço **`os-sistema-api`**
3. Verifique:
   - **Status**: Deve estar "Live" (verde)
   - **Última atualização**: Quando foi atualizado
   - **Logs**: Clique em "Logs" para ver erros

### 2. Verificar Logs da API

Procure nos logs por:

**✅ Sinais de sucesso:**
- `Application startup complete`
- `✅ Schema atualizado com sucesso!`
- `✅ Usuários padrão criados com sucesso!`
- `Uvicorn running on http://0.0.0.0:8000`

**❌ Sinais de erro:**
- `OperationalError` (erro de conexão com banco)
- `ModuleNotFoundError` (dependência faltando)
- `Could not connect to database`
- `FATAL: password authentication failed`

### 3. Verificar Variáveis de Ambiente

No Render → `os-sistema-api` → Environment:

**Verifique se existe:**
- `DATABASE_URL` = `postgresql://postgres:%40Nder0211@db.cowurbzofreatfgwmfwp.supabase.co:5432/postgres`
- `JWT_SECRET` (deve estar configurado)
- `CLOUDINARY_URL` (deve estar configurado)

### 4. Testar API Manualmente

Abra no navegador ou use curl:

```bash
# Health check
curl https://os-sistema-api.onrender.com/health

# Keep-alive
curl https://os-sistema-api.onrender.com/keepalive

# Root
curl https://os-sistema-api.onrender.com/
```

**Se não responder:**
- A API está offline/hibernada
- Precisa acordar ou reiniciar

### 5. Acordar/Reiniciar a API

**Opção A - Acordar automaticamente:**
- O keep-alive do bot deve acordar a API
- Mas se o bot parou, precisa reiniciar manualmente

**Opção B - Reiniciar manualmente:**
1. No Render → `os-sistema-api`
2. Clique em **"Manual Deploy"** → **"Deploy latest commit"**
3. Aguarde 1-2 minutos
4. Verifique os logs

**Opção C - Fazer uma requisição:**
- Acesse `https://os-sistema-api.onrender.com/health` no navegador
- Isso pode acordar a API

### 6. Verificar Conexão com Supabase

Se a API está iniciando mas com erro de banco:

1. Verifique se o `DATABASE_URL` está correto
2. Verifique se o Supabase está ativo
3. Tente usar Session Pooler (porta 6543) se houver erro de IPv4

## 🚀 Após Corrigir

1. **Aguarde** a API iniciar completamente (1-2 minutos)
2. **Teste** acessando `/health` ou `/keepalive`
3. **Reinicie o bot** (ele deve detectar a API automaticamente)
4. **Teste** enviando `/status` para o bot

## 📋 Checklist de Verificação

- [ ] API está "Live" no Render
- [ ] Logs não mostram erros críticos
- [ ] `DATABASE_URL` está configurado corretamente
- [ ] API responde em `/health` ou `/keepalive`
- [ ] Bot consegue fazer heartbeat na API
- [ ] Bot está rodando e respondendo

## 💡 Dica

O keep-alive do bot (`/keepalive` a cada 8 minutos) deve manter a API acordada. Mas se a API não iniciar corretamente, o keep-alive não funciona.

**Prioridade:** Verificar por que a API não está iniciando/respondendo.
