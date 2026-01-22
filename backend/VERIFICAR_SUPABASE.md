# 🔍 Verificação do Supabase

## ⚠️ Erro de DNS/Conectividade

Se você está vendo erro "could not translate host name", pode ser:

1. **Projeto ainda inicializando** (mais comum)
   - Aguarde 2-5 minutos após criar o projeto
   - Verifique no Dashboard se está "Active"

2. **Problema de rede local**
   - Teste de outro computador/rede
   - Ou configure direto no Render/Railway (onde vai rodar)

3. **Firewall/Antivírus**
   - Pode estar bloqueando conexões PostgreSQL
   - Teste desabilitar temporariamente

## ✅ Solução: Configurar Direto no Render/Railway

Como o servidor vai rodar na nuvem mesmo, você pode:

1. **Copiar a string de conexão** do Supabase (já está no .env)
2. **Ir no Render/Railway** → Configurações → Environment Variables
3. **Adicionar**: `DATABASE_URL` = `postgresql://postgres:%40Nder0211@db.cowurbzofreatfgwmfwp.supabase.co:5432/postgres`
4. **Reiniciar** o serviço

O servidor na nuvem vai conseguir conectar normalmente!

## 📋 String de Conexão Configurada

```
postgresql://postgres:%40Nder0211@db.cowurbzofreatfgwmfwp.supabase.co:5432/postgres
```

**Nota:** O `%40` é o `@` codificado na senha.

## 🚀 Próximos Passos

1. ✅ `.env` já está configurado localmente
2. ⏭️ Configure `DATABASE_URL` no Render/Railway
3. ⏭️ Reinicie o serviço
4. ⏭️ Teste criando uma O.S pelo bot
5. ⏭️ Verifique no Supabase Dashboard se os dados aparecem

## 💡 Dica

Se quiser testar localmente depois, pode usar um VPN ou aguardar o projeto finalizar a inicialização no Supabase.
