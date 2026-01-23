# 🚀 Aplicar Migração no Supabase (2 minutos)

## ⚡ Método Rápido

### 1. Acesse o Supabase SQL Editor

1. Abra: **https://supabase.com/dashboard**
2. Faça login
3. Selecione seu projeto
4. No menu lateral, clique em **"SQL Editor"**
5. Clique em **"New query"**

### 2. Cole e Execute

Cole este código SQL e clique em **"Run"**:

```sql
-- Tornar foto_power_meter opcional
ALTER TABLE ordens_servico 
ALTER COLUMN foto_power_meter DROP NOT NULL;

-- Tornar print_os_cliente opcional
ALTER TABLE ordens_servico 
ALTER COLUMN print_os_cliente DROP NOT NULL;

-- Tornar pppoe_cliente opcional
ALTER TABLE ordens_servico 
ALTER COLUMN pppoe_cliente DROP NOT NULL;
```

### 3. Verificar

Execute esta query para confirmar:

```sql
SELECT 
    column_name, 
    is_nullable
FROM information_schema.columns
WHERE table_name = 'ordens_servico'
AND column_name IN ('foto_power_meter', 'print_os_cliente', 'pppoe_cliente')
ORDER BY column_name;
```

**Resultado esperado:**
- Todas as 3 colunas devem mostrar `is_nullable = YES`

---

## ✅ Pronto!

Após aplicar, você pode criar O.S de Rompimento/Manutenções sem erros!

---

**Tempo total: ~2 minutos**
