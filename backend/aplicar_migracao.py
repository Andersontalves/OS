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
# Tentar primeiro .env.supabase (produção), depois .env
if os.path.exists(".env.supabase"):
    load_dotenv(".env.supabase")
    print("[INFO] Usando .env.supabase (producao)")
else:
    load_dotenv()
    print("[INFO] Usando .env")

def aplicar_migracao():
    """Aplica a migração para tornar colunas opcionais"""
    
    # Obter DATABASE_URL do .env
    database_url = os.getenv("DATABASE_URL")
    
    if not database_url:
        print("[ERRO] DATABASE_URL nao encontrado")
        print("   Verifique se existe:")
        print("   - backend/.env.supabase (producao)")
        print("   - backend/.env")
        return False
    
    # Verificar se é SQLite (não suportado para migração)
    if database_url.startswith("sqlite"):
        print("[ERRO] O banco de dados esta configurado como SQLite")
        print("   Esta migracao so funciona com PostgreSQL (Supabase)")
        print()
        print("   Para aplicar a migracao:")
        print("   1. Configure o DATABASE_URL no backend/.env.supabase com a URL do Supabase")
        print("   2. Formato: postgresql://postgres.xxxxx:senha@host:6543/postgres")
        print("   3. Execute o script novamente")
        return False
    
    print("[INFO] Conectando ao banco de dados Supabase...")
    
    try:
        # Conectar ao banco
        conn = psycopg2.connect(database_url)
        cursor = conn.cursor()
        
        print("[OK] Conectado ao banco de dados")
        print()
        
        # Lista de alterações
        alteracoes = [
            ("foto_power_meter", "Tornar foto_power_meter opcional"),
            ("print_os_cliente", "Tornar print_os_cliente opcional"),
            ("pppoe_cliente", "Tornar pppoe_cliente opcional"),
        ]
        
        print("[INFO] Aplicando migracoes...")
        print()
        
        for coluna, descricao in alteracoes:
            try:
                print(f"  - {descricao}...", end=" ")
                
                # Verificar se a coluna já é nullable
                cursor.execute("""
                    SELECT is_nullable
                    FROM information_schema.columns
                    WHERE table_name = 'ordens_servico'
                    AND column_name = %s
                """, (coluna,))
                
                result = cursor.fetchone()
                if result and result[0] == 'YES':
                    print("[OK] Ja e opcional")
                else:
                    # Aplicar ALTER TABLE
                    query = sql.SQL("ALTER TABLE ordens_servico ALTER COLUMN {} DROP NOT NULL").format(
                        sql.Identifier(coluna)
                    )
                    cursor.execute(query)
                    print("[OK] Aplicado")
                    
            except Exception as e:
                print(f"[ERRO] {str(e)}")
                conn.rollback()
                return False
        
        # Commit das alterações
        conn.commit()
        print()
        print("[OK] Migracao aplicada com sucesso!")
        print()
        
        # Verificar resultado
        print("[INFO] Verificando alteracoes...")
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
            status = "[OK] Opcional" if nullable == 'YES' else "[ERRO] Obrigatorio"
            print(f"  {coluna:20} | {tipo:15} | {status}")
        print("-" * 60)
        
        cursor.close()
        conn.close()
        
        return True
        
    except psycopg2.OperationalError as e:
        print(f"[ERRO] Erro de conexao: {str(e)}")
        print()
        print("Verifique:")
        print("  1. O DATABASE_URL esta correto no arquivo .env?")
        print("  2. Voce tem acesso a internet?")
        print("  3. O Supabase esta acessivel?")
        return False
        
    except Exception as e:
        print(f"[ERRO] {str(e)}")
        return False

if __name__ == "__main__":
    print("=" * 60)
    print("  MIGRACAO: Colunas Opcionais")
    print("=" * 60)
    print()
    
    sucesso = aplicar_migracao()
    
    if sucesso:
        print()
        print("[OK] Migracao concluida com sucesso!")
        print("   Agora voce pode criar O.S de Rompimento/Manutencoes")
    else:
        print()
        print("[ERRO] Migracao falhou. Verifique os erros acima.")
        sys.exit(1)
