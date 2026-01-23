# 🔧 Aplicar Migração: Colunas Opcionais

## ❌ Problema

O banco de dados está rejeitando O.S de Rompimento/Manutenções porque as colunas `foto_power_meter`, `print_os_cliente` e `pppoe_cliente` estão definidas como `NOT NULL`, mas esses campos não são preenchidos para esses tipos de O.S.

## ✅ Solução

Execute a migração SQL no Supabase para tornar essas colunas opcionais.

---

## 📋 Passo a Passo

### 1. Acessar o Supabase

1. Acesse: https://supabase.com/dashboard
2. Faça login
3. Selecione seu projeto

### 2. Abrir SQL Editor

1. No menu lateral, clique em **"SQL Editor"**
2. Clique em **"New query"**

### 3. Executar a Migração

1. Abra o arquivo: `backend/MIGRAR_COLUNAS_OPCIONAIS.sql`
2. Copie todo o conteúdo do arquivo
3. Cole no SQL Editor do Supabase
4. Clique em **"Run"** ou pressione `Ctrl+Enter`

### 4. Verificar

Após executar, você deve ver uma tabela mostrando que as colunas agora são `nullable = YES`.

---

## 🔍 Verificar se Funcionou

Execute esta query no Supabase para confirmar:

```sql
SELECT 
    column_name, 
    is_nullable,
    data_type
FROM information_schema.columns
WHERE table_name = 'ordens_servico'
AND column_name IN ('foto_power_meter', 'print_os_cliente', 'pppoe_cliente')
ORDER BY column_name;
```

**Resultado esperado:**
- `foto_power_meter`: `is_nullable = YES`
- `print_os_cliente`: `is_nullable = YES`
- `pppoe_cliente`: `is_nullable = YES`

---

## ⚠️ Importante

- Esta migração **não apaga dados existentes**
- Apenas permite que essas colunas sejam `NULL` em novas O.S
- O.S antigas continuam funcionando normalmente

---

## 🆘 Problemas?

Se der erro ao executar, verifique:
1. Você tem permissão de administrador no Supabase?
2. O nome da tabela está correto? (`ordens_servico`)
3. As colunas existem na tabela?

---

**Após aplicar a migração, teste criar uma O.S de Rompimento novamente!**
