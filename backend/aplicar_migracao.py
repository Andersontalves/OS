"""
Script para aplicar migração: tornar colunas opcionais no banco de dados
Execute: python aplicar_migracao.py
"""
import os
import sys
from dotenv import load_dotenv
import psycopg2
from psycopg2 import sql

# Carregar variáveis de ambiente
load_dotenv()

def aplicar_migracao():
    """Aplica a migração para tornar colunas opcionais"""
    
    # Obter DATABASE_URL do .env
    database_url = os.getenv("DATABASE_URL")
    
    if not database_url:
        print("❌ ERRO: DATABASE_URL não encontrado no arquivo .env")
        print("   Certifique-se de que o arquivo backend/.env existe e contém DATABASE_URL")
        return False
    
    print("🔌 Conectando ao banco de dados...")
    
    try:
        # Conectar ao banco
        conn = psycopg2.connect(database_url)
        cursor = conn.cursor()
        
        print("✅ Conectado ao banco de dados")
        print()
        
        # Lista de alterações
        alteracoes = [
            ("foto_power_meter", "Tornar foto_power_meter opcional"),
            ("print_os_cliente", "Tornar print_os_cliente opcional"),
            ("pppoe_cliente", "Tornar pppoe_cliente opcional"),
        ]
        
        print("📝 Aplicando migrações...")
        print()
        
        for coluna, descricao in alteracoes:
            try:
                print(f"  • {descricao}...", end=" ")
                
                # Verificar se a coluna já é nullable
                cursor.execute("""
                    SELECT is_nullable
                    FROM information_schema.columns
                    WHERE table_name = 'ordens_servico'
                    AND column_name = %s
                """, (coluna,))
                
                result = cursor.fetchone()
                if result and result[0] == 'YES':
                    print("✅ Já é opcional")
                else:
                    # Aplicar ALTER TABLE
                    query = sql.SQL("ALTER TABLE ordens_servico ALTER COLUMN {} DROP NOT NULL").format(
                        sql.Identifier(coluna)
                    )
                    cursor.execute(query)
                    print("✅ Aplicado")
                    
            except Exception as e:
                print(f"❌ Erro: {str(e)}")
                conn.rollback()
                return False
        
        # Commit das alterações
        conn.commit()
        print()
        print("✅ Migração aplicada com sucesso!")
        print()
        
        # Verificar resultado
        print("🔍 Verificando alterações...")
        cursor.execute("""
            SELECT 
                column_name, 
                is_nullable,
                data_type
            FROM information_schema.columns
            WHERE table_name = 'ordens_servico'
            AND column_name IN ('foto_power_meter', 'print_os_cliente', 'pppoe_cliente')
            ORDER BY column_name
        """)
        
        resultados = cursor.fetchall()
        print()
        print("Resultado:")
        print("-" * 60)
        for coluna, nullable, tipo in resultados:
            status = "✅ Opcional" if nullable == 'YES' else "❌ Obrigatório"
            print(f"  {coluna:20} | {tipo:15} | {status}")
        print("-" * 60)
        
        cursor.close()
        conn.close()
        
        return True
        
    except psycopg2.OperationalError as e:
        print(f"❌ ERRO de conexão: {str(e)}")
        print()
        print("Verifique:")
        print("  1. O DATABASE_URL está correto no arquivo .env?")
        print("  2. Você tem acesso à internet?")
        print("  3. O Supabase está acessível?")
        return False
        
    except Exception as e:
        print(f"❌ ERRO: {str(e)}")
        return False

if __name__ == "__main__":
    print("=" * 60)
    print("  MIGRAÇÃO: Colunas Opcionais")
    print("=" * 60)
    print()
    
    sucesso = aplicar_migracao()
    
    if sucesso:
        print()
        print("✅ Migração concluída com sucesso!")
        print("   Agora você pode criar O.S de Rompimento/Manutenções")
    else:
        print()
        print("❌ Migração falhou. Verifique os erros acima.")
        sys.exit(1)
