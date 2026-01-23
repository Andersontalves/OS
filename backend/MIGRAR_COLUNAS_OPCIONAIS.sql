-- Migração: Tornar colunas opcionais para Rompimento/Manutenções
-- Execute este script no Supabase SQL Editor

-- Tornar foto_power_meter opcional (não é pedido para rompimento/manutenção)
ALTER TABLE ordens_servico 
ALTER COLUMN foto_power_meter DROP NOT NULL;

-- Tornar print_os_cliente opcional (não é pedido para rompimento/manutenção)
ALTER TABLE ordens_servico 
ALTER COLUMN print_os_cliente DROP NOT NULL;

-- Tornar pppoe_cliente opcional (não é pedido para rompimento)
ALTER TABLE ordens_servico 
ALTER COLUMN pppoe_cliente DROP NOT NULL;

-- Verificar se as alterações foram aplicadas
SELECT 
    column_name, 
    is_nullable,
    data_type
FROM information_schema.columns
WHERE table_name = 'ordens_servico'
AND column_name IN ('foto_power_meter', 'print_os_cliente', 'pppoe_cliente')
ORDER BY column_name;
