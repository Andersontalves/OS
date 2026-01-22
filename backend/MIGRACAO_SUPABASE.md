# 🚀 Guia de Migração para Supabase (Postgres Free)

Este guia mostra como migrar do SQLite para Supabase Postgres gratuitamente.

## 📋 Pré-requisitos

1. Conta no Supabase (gratuita): https://supabase.com
2. Python 3.8+ instalado
3. Dependências instaladas: `pip install -r requirements.txt`

## 🔧 Passo 1: Criar Projeto no Supabase

1. Acesse https://supabase.com e faça login
2. Clique em "New Project"
3. Preencha:
   - **Name**: `os-sistema` (ou outro nome)
   - **Database Password**: Crie uma senha forte (anote!)
   - **Region**: Escolha a mais próxima (ex: South America)
4. Aguarde a criação (2-3 minutos)

## 📝 Passo 2: Obter String de Conexão

1. No projeto Supabase, vá em **Settings** → **Database**
2. Role até **Connection string** → **URI**
3. Copie a string (formato: `postgresql://postgres:[PASSWORD]@[HOST]:5432/postgres`)
4. Substitua `[PASSWORD]` pela senha que você criou

**Exemplo:**
```
postgresql://postgres.xxxxx:senha123@aws-0-sa-east-1.pooler.supabase.com:6543/postgres
```

## 💾 Passo 3: Fazer Backup do SQLite Atual

```bash
cd backend
python backup_sqlite.py
```

Isso criará dois arquivos:
- `backup_sqlite_YYYYMMDD_HHMMSS.sql` (backup completo)
- `backup_sqlite_YYYYMMDD_HHMMSS.json` (usado para migração)

## 🔄 Passo 4: Migrar Dados para Supabase

1. Edite o arquivo `.env` no backend:
```env
DATABASE_URL=postgresql://postgres.xxxxx:senha123@aws-0-sa-east-1.pooler.supabase.com:6543/postgres
```

2. Execute a migração:
```bash
python migrate_to_supabase.py
```

Ou especifique o arquivo de backup:
```bash
python migrate_to_supabase.py backup_sqlite_20240101_120000.json
```

## ✅ Passo 5: Verificar Migração

1. No Supabase, vá em **Table Editor**
2. Verifique se as tabelas `users` e `ordens_servico` foram criadas
3. Confira se os dados foram importados corretamente

## 🚀 Passo 6: Atualizar Backend

O backend já está configurado para usar `DATABASE_URL` do `.env`. 

**Para Render/Railway:**
1. Vá nas configurações do serviço
2. Adicione a variável `DATABASE_URL` com a string do Supabase
3. Reinicie o serviço

**Para local:**
1. Atualize o `.env` com a nova `DATABASE_URL`
2. Reinicie o servidor

## 🔍 Verificação Final

1. Teste o endpoint `/health` do backend
2. Teste criar uma nova O.S pelo bot
3. Verifique no Supabase se os dados aparecem

## ⚠️ Importante

- **Backup**: Mantenha os arquivos de backup por segurança
- **Senha**: Guarde a senha do Supabase em local seguro
- **Limites Free**: 
  - 500 MB de banco
  - 2 GB de transferência/mês
  - Sem limite de tempo (permanente)

## 🆘 Troubleshooting

**Erro de conexão:**
- Verifique se a senha está correta na string de conexão
- Use a string de **Connection pooling** (porta 6543) para melhor performance

**Erro na migração:**
- Verifique se as tabelas existem no Supabase
- Execute `python init_db.py` primeiro para criar o schema

**Dados duplicados:**
- O script usa `ON CONFLICT DO NOTHING` para evitar duplicatas
- Se precisar refazer, delete as tabelas no Supabase primeiro

## 📞 Suporte

Se tiver problemas, verifique:
1. Logs do backend
2. Logs do Supabase (Dashboard → Logs)
3. Arquivo de backup JSON
