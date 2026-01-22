# ⚡ Quick Start - Supabase (5 minutos)

## 🎯 Objetivo
Migrar do SQLite para Supabase Postgres gratuitamente e garantir que o servidor não pare.

## 📋 Checklist Rápido

- [ ] Criar projeto no Supabase
- [ ] Obter string de conexão
- [ ] Fazer backup (se tiver dados)
- [ ] Executar script de setup
- [ ] Atualizar Render/Railway
- [ ] Testar

## 🚀 Execução Automática

Execute o script interativo que guia tudo:

```bash
cd backend
python setup_supabase.py
```

O script vai te guiar passo a passo!

## 📝 Ou faça manualmente:

### 1. Criar Projeto Supabase (2 min)
- https://supabase.com → New Project
- Nome: `os-sistema`
- Senha: (anote!)
- Region: South America

### 2. Obter String (1 min)
- Settings → Database → Connection string → URI
- Copie e substitua `[PASSWORD]` pela senha

### 3. Backup (1 min)
```bash
python backup_sqlite.py
```

### 4. Configurar (1 min)
```bash
python setup_supabase.py
```

Ou edite `.env` manualmente:
```env
DATABASE_URL=postgresql://postgres.xxxxx:SENHA@host:6543/postgres
```

### 5. Criar Schema
```bash
python init_db.py
```

### 6. Migrar Dados (se houver backup)
```bash
python migrate_to_supabase.py
```

### 7. Atualizar Render/Railway
- Configurações → Environment Variables
- Adicionar: `DATABASE_URL` = string do Supabase
- Reiniciar serviço

### 8. Testar
```bash
python test_database.py
```

## ✅ Verificação

- ✅ Backend conecta ao Supabase
- ✅ Bot funciona normalmente  
- ✅ Dados aparecem no Supabase Dashboard
- ✅ Servidor não para mais!

## 🆘 Problemas?

**Erro de conexão:**
- Verifique a senha na string
- Use porta 6543 (pooler)

**Script não funciona:**
- Execute manualmente os passos acima
- Veja `MIGRACAO_SUPABASE.md` para guia completo
