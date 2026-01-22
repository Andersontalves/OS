"""
Script para fazer backup do banco SQLite atual
Gera arquivos SQL e JSON para importação posterior
"""
import sqlite3
import json
import os
import sys
from datetime import datetime
from pathlib import Path

# Fix encoding for Windows
if sys.platform == 'win32':
    import codecs
    sys.stdout = codecs.getwriter('utf-8')(sys.stdout.buffer, 'strict')
    sys.stderr = codecs.getwriter('utf-8')(sys.stderr.buffer, 'strict')

def backup_sqlite_to_sql(db_path: str = "os_database.db", output_file: str = None):
    """Faz backup do SQLite para arquivo SQL"""
    if output_file is None:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_file = f"backup_sqlite_{timestamp}.sql"
    
    conn = sqlite3.connect(db_path)
    
    with open(output_file, 'w', encoding='utf-8') as f:
        for line in conn.iterdump():
            f.write(f'{line}\n')
    
    conn.close()
    print(f"OK: Backup SQL criado: {output_file}")
    return output_file

def backup_sqlite_to_json(db_path: str = "os_database.db", output_file: str = None):
    """Faz backup do SQLite para arquivo JSON (mais fácil de importar)"""
    if output_file is None:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_file = f"backup_sqlite_{timestamp}.json"
    
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    
    backup_data = {
        "timestamp": datetime.now().isoformat(),
        "tables": {}
    }
    
    # Backup tabela users
    users = conn.execute("SELECT * FROM users").fetchall()
    backup_data["tables"]["users"] = [dict(row) for row in users]
    
    # Backup tabela ordens_servico
    ordens = conn.execute("SELECT * FROM ordens_servico").fetchall()
    backup_data["tables"]["ordens_servico"] = [dict(row) for row in ordens]
    
    conn.close()
    
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(backup_data, f, indent=2, ensure_ascii=False, default=str)
    
    print(f"OK: Backup JSON criado: {output_file}")
    print(f"   - {len(backup_data['tables']['users'])} usuarios")
    print(f"   - {len(backup_data['tables']['ordens_servico'])} ordens de servico")
    return output_file

if __name__ == "__main__":
    print("Iniciando backup do banco SQLite...")
    
    db_path = os.path.join(os.path.dirname(__file__), "os_database.db")
    
    if not os.path.exists(db_path):
        print(f"AVISO: Arquivo nao encontrado: {db_path}")
        print("   O banco pode estar vazio ou nao ter sido criado ainda.")
        print("   Continuando mesmo assim...")
        # Cria backups vazios para manter consistência
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        sql_file = f"backup_sqlite_{timestamp}.sql"
        json_file = f"backup_sqlite_{timestamp}.json"
        with open(sql_file, 'w') as f:
            f.write("-- Banco SQLite vazio ou nao encontrado\n")
        with open(json_file, 'w') as f:
            json.dump({"timestamp": datetime.now().isoformat(), "tables": {"users": [], "ordens_servico": []}}, f, indent=2)
        print(f"OK: Backups vazios criados")
        print(f"   SQL: {sql_file}")
        print(f"   JSON: {json_file}")
        exit(0)
    
    # Backup em ambos os formatos
    sql_file = backup_sqlite_to_sql(db_path)
    json_file = backup_sqlite_to_json(db_path)
    
    print("\nOK: Backup concluido!")
    print(f"   SQL: {sql_file}")
    print(f"   JSON: {json_file}")
    print("\nDica: Use o arquivo JSON para importar no Supabase.")
