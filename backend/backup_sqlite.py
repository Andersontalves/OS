"""
Script para fazer backup do banco SQLite atual
Gera arquivos SQL e JSON para importação posterior
"""
import sqlite3
import json
import os
from datetime import datetime
from pathlib import Path

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
    print(f"✅ Backup SQL criado: {output_file}")
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
    
    print(f"✅ Backup JSON criado: {output_file}")
    print(f"   - {len(backup_data['tables']['users'])} usuários")
    print(f"   - {len(backup_data['tables']['ordens_servico'])} ordens de serviço")
    return output_file

if __name__ == "__main__":
    print("🔄 Iniciando backup do banco SQLite...")
    
    db_path = os.path.join(os.path.dirname(__file__), "os_database.db")
    
    if not os.path.exists(db_path):
        print(f"❌ Arquivo não encontrado: {db_path}")
        print("   Verifique se o banco existe ou ajuste o caminho.")
        exit(1)
    
    # Backup em ambos os formatos
    sql_file = backup_sqlite_to_sql(db_path)
    json_file = backup_sqlite_to_json(db_path)
    
    print("\n✅ Backup concluído!")
    print(f"   SQL: {sql_file}")
    print(f"   JSON: {json_file}")
    print("\n💡 Use o arquivo JSON para importar no Supabase.")
