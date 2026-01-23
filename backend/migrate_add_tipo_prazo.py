"""
Script para adicionar campos tipo_os, prazo e porta_placa_olt ao banco existente
- Define todas as O.S existentes como tipo_os="normal"
- Adiciona colunas tipo_os, prazo_horas, prazo_fim, porta_placa_olt
"""
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from sqlalchemy import text
from app.database import engine

def migrate():
    print("🔄 Iniciando migração...")
    
    try:
        with engine.begin() as conn:
            # Adicionar colunas se não existirem
            print("📝 Adicionando coluna tipo_os...")
            conn.execute(text("""
                ALTER TABLE ordens_servico 
                ADD COLUMN IF NOT EXISTS tipo_os VARCHAR(20) DEFAULT 'normal'
            """))
            
            print("📝 Adicionando coluna prazo_horas...")
            conn.execute(text("""
                ALTER TABLE ordens_servico 
                ADD COLUMN IF NOT EXISTS prazo_horas INTEGER
            """))
            
            print("📝 Adicionando coluna prazo_fim...")
            conn.execute(text("""
                ALTER TABLE ordens_servico 
                ADD COLUMN IF NOT EXISTS prazo_fim TIMESTAMP
            """))
            
            print("📝 Adicionando coluna porta_placa_olt...")
            conn.execute(text("""
                ALTER TABLE ordens_servico 
                ADD COLUMN IF NOT EXISTS porta_placa_olt VARCHAR(50)
            """))
            
            # Atualizar O.S existentes
            print("🔄 Atualizando O.S existentes...")
            conn.execute(text("""
                UPDATE ordens_servico 
                SET tipo_os = 'normal' 
                WHERE tipo_os IS NULL
            """))
            
            # Adicionar constraint se não existir
            print("📝 Adicionando constraint check_tipo_os_valido...")
            try:
                conn.execute(text("""
                    ALTER TABLE ordens_servico 
                    DROP CONSTRAINT IF EXISTS check_tipo_os_valido
                """))
            except:
                pass
            
            conn.execute(text("""
                ALTER TABLE ordens_servico 
                ADD CONSTRAINT check_tipo_os_valido 
                CHECK (tipo_os IN ('normal', 'rompimento', 'manutencao'))
            """))
            
            print("✅ Migração concluída com sucesso!")
            
    except Exception as e:
        print(f"❌ Erro na migração: {e}")
        raise

if __name__ == "__main__":
    migrate()
