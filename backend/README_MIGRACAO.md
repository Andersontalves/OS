# 🚀 Migração Rápida para Supabase (15 dias)

## ⚡ Resumo Rápido

1. **Criar projeto no Supabase** (2 min)
2. **Fazer backup do SQLite** (1 min)
3. **Migrar dados** (2 min)
4. **Atualizar DATABASE_URL** (1 min)
5. **Pronto!** ✅

**Tempo total: ~6 minutos**

## 📋 Passo a Passo

### 1. Criar Projeto Supabase

1. Acesse: https://supabase.com
2. Login → New Project
3. Nome: `os-sistema`
4. Senha: (anote bem!)
5. Region: South America
6. Aguarde criação

### 2. Obter String de Conexão

1. Settings → Database
2. Connection string → URI
3. Copie a string completa
4. Substitua `[PASSWORD]` pela sua senha

**Exemplo:**
```
postgresql://postgres.xxxxx:SUA_SENHA@aws-0-sa-east-1.pooler.supabase.com:6543/postgres
```

### 3. Fazer Backup

```bash
cd backend
python backup_sqlite.py
```

### 4. Migrar Dados

1. Edite `.env` e adicione:
```env
DATABASE_URL=postgresql://postgres.xxxxx:SUA_SENHA@aws-0-sa-east-1.pooler.supabase.com:6543/postgres
```

2. Execute migração:
```bash
python migrate_to_supabase.py
```

### 5. Criar Schema (se necessário)

```bash
python init_db.py
```

### 6. Testar Conexão

```bash
python test_database.py
```

### 7. Atualizar Render/Railway

1. Vá nas configurações do serviço
2. Adicione variável: `DATABASE_URL`
3. Cole a string do Supabase
4. Reinicie o serviço

## ✅ Verificação

- ✅ Backend conecta ao Supabase
- ✅ Bot funciona normalmente
- ✅ Dados aparecem no Supabase Dashboard

## 📁 Arquivos Criados

- `backup_sqlite.py` - Faz backup do SQLite
- `migrate_to_supabase.py` - Migra dados para Supabase
- `test_database.py` - Testa conexão
- `MIGRACAO_SUPABASE.md` - Guia completo

## 🆘 Problemas?

**Erro de conexão:**
- Verifique a senha na string
- Use porta 6543 (pooler)

**Dados não aparecem:**
- Execute `python init_db.py` primeiro
- Verifique logs do script de migração

**Backend não conecta:**
- Verifique `DATABASE_URL` no `.env`
- Teste com `python test_database.py`
