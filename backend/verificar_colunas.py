"""Verificar se as colunas necessárias existem no banco"""
from app.database import engine, Base
from sqlalchemy import text, inspect

# Criar todas as tabelas (isso adiciona colunas que faltam)
Base.metadata.create_all(bind=engine)

# Verificar colunas da tabela ordens_servico
inspector = inspect(engine)
columns = inspector.get_columns('ordens_servico')
col_names = [col['name'] for col in columns]

print("Colunas na tabela ordens_servico:")
for col in col_names:
    print(f"  - {col}")

print("\nVerificacao:")
print(f"  tipo_os: {'tipo_os' in col_names}")
print(f"  prazo_horas: {'prazo_horas' in col_names}")
print(f"  prazo_fim: {'prazo_fim' in col_names}")
print(f"  porta_placa_olt: {'porta_placa_olt' in col_names}")
print(f"  cidade: {'cidade' in col_names}")
