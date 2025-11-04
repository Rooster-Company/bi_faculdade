"""
Script para converter banco de dados Access (.accdb) para SQLite
"""
import pyodbc
import sqlite3
import os

def convert_access_to_sqlite(accdb_path, sqlite_path):
    """
    Converte banco Access para SQLite
    """
    # Conectar ao Access
    conn_str = (
        r'DRIVER={Microsoft Access Driver (*.mdb, *.accdb)};'
        f'DBQ={accdb_path};'
    )
    
    try:
        access_conn = pyodbc.connect(conn_str)
        access_cursor = access_conn.cursor()
        
        # Criar banco SQLite
        sqlite_conn = sqlite3.connect(sqlite_path)
        sqlite_cursor = sqlite_conn.cursor()
        
        # Obter lista de tabelas
        tables = [table.table_name for table in access_cursor.tables(tableType='TABLE')]
        
        print(f"Tabelas encontradas: {tables}")
        
        for table in tables:
            if table.startswith('MSys'):  # Ignorar tabelas de sistema
                continue
                
            print(f"\nProcessando tabela: {table}")
            
            # Obter dados da tabela
            access_cursor.execute(f"SELECT * FROM [{table}]")
            columns = [column[0] for column in access_cursor.description]
            rows = access_cursor.fetchall()
            
            if not rows:
                print(f"  Tabela {table} está vazia")
                continue
            
            # Criar tabela no SQLite
            placeholders = ', '.join(['?' for _ in columns])
            columns_def = ', '.join([f'"{col}" TEXT' for col in columns])
            
            sqlite_cursor.execute(f'DROP TABLE IF EXISTS "{table}"')
            sqlite_cursor.execute(f'CREATE TABLE "{table}" ({columns_def})')
            
            # Inserir dados
            insert_sql = f'INSERT INTO "{table}" VALUES ({placeholders})'
            sqlite_cursor.executemany(insert_sql, rows)
            
            print(f"  {len(rows)} registros inseridos")
        
        sqlite_conn.commit()
        print(f"\n✅ Conversão concluída! Banco SQLite criado em: {sqlite_path}")
        
        access_conn.close()
        sqlite_conn.close()
        
    except pyodbc.Error as e:
        print(f"❌ Erro ao conectar ao Access: {e}")
        print("\nNOTA: Em Linux, pyodbc não suporta Access diretamente.")
        print("Você pode usar mdb-tools ou fazer a conversão no Windows.")
        return False
    
    return True

if __name__ == "__main__":
    accdb_file = "db.accdb"
    sqlite_file = "vendas.db"
    
    if not os.path.exists(accdb_file):
        print(f"❌ Arquivo {accdb_file} não encontrado!")
    else:
        convert_access_to_sqlite(accdb_file, sqlite_file)
