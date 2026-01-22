# 🔧 Configurar Supabase no Render/Railway

## 📋 Serviços que precisam de configuração

1. **`os-sistema-api`** (Backend) - Precisa do `DATABASE_URL`
2. **`os-sistema-bot`** (Bot Telegram) - NÃO precisa do `DATABASE_URL` (só usa a API)

## ✅ Passo a Passo

### 1. Configurar `os-sistema-api` (Backend)

1. Acesse o serviço **`os-sistema-api`** no Render/Railway
2. Vá em **Environment** ou **Environment Variables**
3. Procure por `DATABASE_URL` ou adicione uma nova variável:
   - **Nome:** `DATABASE_URL`
   - **Valor:** `postgresql://postgres:%40Nder0211@db.cowurbzofreatfgwmfwp.supabase.co:5432/postgres`
4. Salve as alterações
5. O serviço vai reiniciar automaticamente

### 2. Verificar `os-sistema-bot` (Bot)

O bot **NÃO precisa** do `DATABASE_URL` porque ele só faz requisições HTTP para a API.

Mas verifique se ele tem:
- `API_BASE_URL` apontando para o `os-sistema-api`
- `TELEGRAM_BOT_TOKEN` configurado

### 3. Após reiniciar o `os-sistema-api`

1. **Aguarde** o serviço reiniciar (1-2 minutos)
2. **Verifique os logs** do `os-sistema-api`:
   - Deve conectar ao Supabase
   - Criará as tabelas automaticamente (se não existirem)
3. **Teste** criando uma O.S pelo bot do Telegram

### 4. Migrar dados (opcional)

Se quiser migrar os dados do backup:

1. Execute localmente (quando conseguir conectar):
   ```bash
   cd backend
   python migrate_to_supabase.py backup_sqlite_20260122_194850.json
   ```

2. Ou aguarde - os dados serão criados naturalmente pelo uso do sistema

## 📝 String de Conexão Completa

```
DATABASE_URL=postgresql://postgres:%40Nder0211@db.cowurbzofreatfgwmfwp.supabase.co:5432/postgres
```

**Importante:** O `%40` é o `@` codificado na senha. Não altere isso!

## ✅ Checklist

- [ ] `DATABASE_URL` configurado no `os-sistema-api`
- [ ] Serviço `os-sistema-api` reiniciado
- [ ] Logs mostram conexão bem-sucedida
- [ ] Teste criando uma O.S pelo bot
- [ ] Verificar dados no Supabase Dashboard

## 🐛 Troubleshooting

**Se o serviço não conectar:**
1. Verifique se a string está exatamente como acima
2. Verifique os logs do `os-sistema-api`
3. Confirme que o projeto Supabase está ativo
4. Tente usar o Session Pooler (porta 6543) se houver erro de IPv4

**Session Pooler (alternativa):**
```
DATABASE_URL=postgresql://postgres.cowurbzofreatfgwmfwp:%40Nder0211@aws-0-sa-east-1.pooler.supabase.com:6543/postgres
```
