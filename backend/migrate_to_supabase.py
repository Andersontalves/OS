"""
Script para migrar dados do SQLite para Supabase Postgres
Execute após criar o projeto no Supabase e configurar DATABASE_URL
"""
import os
import json
import sys
from sqlalchemy import create_engine, text
from sqlalchemy.orm import Session
from dotenv import load_dotenv

# Fix encoding for Windows
if sys.platform == 'win32':
    import codecs
    sys.stdout = codecs.getwriter('utf-8')(sys.stdout.buffer, 'strict')
    sys.stderr = codecs.getwriter('utf-8')(sys.stderr.buffer, 'strict')

# Carrega variáveis de ambiente
load_dotenv()

def load_backup_json(backup_file: str):
    """Carrega dados do backup JSON"""
    with open(backup_file, 'r', encoding='utf-8') as f:
        return json.load(f)

def migrate_to_supabase(backup_file: str = None, database_url: str = None):
    """Migra dados do backup para Supabase"""
    
    # Usa DATABASE_URL do .env ou pede para o usuário
    if database_url is None:
        database_url = os.getenv("DATABASE_URL")
    
    if not database_url:
        print("ERRO: DATABASE_URL nao configurado!")
        print("   Configure no .env ou passe como parametro.")
        print("   Exemplo: postgresql://user:pass@host:5432/dbname")
        return False
    
    # Encontra o arquivo de backup mais recente
    if backup_file is None:
        backup_files = [f for f in os.listdir('.') if f.startswith('backup_sqlite_') and f.endswith('.json')]
        if not backup_files:
            print("ERRO: Nenhum arquivo de backup encontrado!")
            print("   Execute primeiro: python backup_sqlite.py")
            return False
        backup_file = sorted(backup_files)[-1]  # Mais recente
        print(f"Usando backup: {backup_file}")
    
    # Carrega backup
    print("Carregando backup...")
    backup_data = load_backup_json(backup_file)
    
    # Conecta ao Supabase
    print("Conectando ao Supabase...")
    engine = create_engine(database_url)
    
    with Session(engine) as session:
        try:
            # Migra usuários
            print("Migrando usuarios...")
            users = backup_data["tables"].get("users", [])
            for user_data in users:
                # Cria cópia para não modificar o original
                user_insert = user_data.copy()
                user_id = user_insert.pop('id', None)
                session.execute(
                    text("""
                        INSERT INTO users (username, password_hash, role, telegram_id, nome, created_at)
                        VALUES (:username, :password_hash, :role, :telegram_id, :nome, :created_at)
                        ON CONFLICT (username) DO NOTHING
                    """),
                    user_insert
                )
            session.commit()
            print(f"   OK: {len(users)} usuarios migrados")
            
            # Migra ordens de serviço
            print("Migrando ordens de servico...")
            ordens = backup_data["tables"].get("ordens_servico", [])
            
            # Primeiro, mapeia IDs antigos para novos (baseado em username)
            user_id_map = {}
            for old_id in set(o.get('tecnico_campo_id') for o in ordens if o.get('tecnico_campo_id')):
                result = session.execute(
                    text("SELECT id FROM users WHERE id = :old_id"),
                    {"old_id": old_id}
                ).first()
                if result:
                    user_id_map[old_id] = result[0]
            
            for ordem_data in ordens:
                ordem_insert = ordem_data.copy()
                ordem_id = ordem_insert.pop('id', None)
                # Atualiza IDs de técnicos
                if ordem_insert.get('tecnico_campo_id') in user_id_map:
                    ordem_insert['tecnico_campo_id'] = user_id_map[ordem_insert['tecnico_campo_id']]
                if ordem_insert.get('tecnico_executor_id') in user_id_map:
                    ordem_insert['tecnico_executor_id'] = user_id_map[ordem_insert['tecnico_executor_id']]
                
                session.execute(
                    text("""
                        INSERT INTO ordens_servico (
                            numero_os, tecnico_campo_id, foto_power_meter, foto_caixa,
                            localizacao_lat, localizacao_lng, localizacao_precisao,
                            print_os_cliente, pppoe_cliente, motivo_abertura,
                            telegram_nick, telegram_phone, cidade, status,
                            tecnico_executor_id, criado_em, iniciado_em, concluido_em,
                            foto_comprovacao, observacoes
                        )
                        VALUES (
                            :numero_os, :tecnico_campo_id, :foto_power_meter, :foto_caixa,
                            :localizacao_lat, :localizacao_lng, :localizacao_precisao,
                            :print_os_cliente, :pppoe_cliente, :motivo_abertura,
                            :telegram_nick, :telegram_phone, :cidade, :status,
                            :tecnico_executor_id, :criado_em, :iniciado_em, :concluido_em,
                            :foto_comprovacao, :observacoes
                        )
                        ON CONFLICT (numero_os) DO NOTHING
                    """),
                    ordem_insert
                )
            session.commit()
            print(f"   OK: {len(ordens)} ordens migradas")
            
            print("\nOK: Migracao concluida com sucesso!")
            return True
            
        except Exception as e:
            session.rollback()
            print(f"\nERRO na migracao: {e}")
            import traceback
            traceback.print_exc()
            return False

if __name__ == "__main__":
    print("Migracao SQLite -> Supabase Postgres\n")
    
    backup_file = sys.argv[1] if len(sys.argv) > 1 else None
    database_url = sys.argv[2] if len(sys.argv) > 2 else None
    
    success = migrate_to_supabase(backup_file, database_url)
    
    if success:
        print("\nProximos passos:")
        print("   1. DATABASE_URL ja esta configurado no .env")
        print("   2. Reinicie o backend")
        print("   3. Teste a aplicacao")
    else:
        print("\nERRO: Migracao falhou. Verifique os erros acima.")
        sys.exit(1)
