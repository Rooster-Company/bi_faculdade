"""
Teste 1: Validação da Estrutura do Banco de Dados
Verifica se todas as entidades obrigatórias estão presentes e corretamente estruturadas
"""
import sqlite3
import sys

def test_database_structure():
    """Testa a estrutura completa do banco de dados"""
    
    print("=" * 80)
    print("TESTE 1: ESTRUTURA DO BANCO DE DADOS")
    print("=" * 80)
    
    conn = sqlite3.connect('vendas.db')
    cursor = conn.cursor()
    
    all_tests_passed = True
    
    # Teste 1: Verificar existência das tabelas
    print("\n📋 1.1. Verificando existência das tabelas obrigatórias...")
    
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' ORDER BY name")
    tables = [row[0] for row in cursor.fetchall()]
    
    required_tables = ['Veiculos', 'Vendas', 'Vendedores', 'Clientes', 'Regioes']
    
    for table in required_tables:
        if table in tables:
            print(f"   ✅ Tabela '{table}' encontrada")
        else:
            print(f"   ❌ ERRO: Tabela '{table}' NÃO encontrada")
            all_tests_passed = False
    
    # Teste 2: Verificar estrutura da tabela Veiculos
    print("\n🚗 1.2. Verificando estrutura da tabela 'Veiculos'...")
    cursor.execute("PRAGMA table_info(Veiculos)")
    columns = {row[1]: row[2] for row in cursor.fetchall()}
    
    required_columns = {
        'ID': 'INTEGER',
        'Modelo': 'TEXT',
        'Marca': 'TEXT',
        'Categoria': 'TEXT',
        'Cor': 'TEXT',
        'PrecoUnitario': 'REAL'
    }
    
    for col, col_type in required_columns.items():
        if col in columns:
            print(f"   ✅ Coluna '{col}' ({col_type}) encontrada")
        else:
            print(f"   ❌ ERRO: Coluna '{col}' NÃO encontrada")
            all_tests_passed = False
    
    # Teste 3: Verificar estrutura da tabela Vendas
    print("\n💰 1.3. Verificando estrutura da tabela 'Vendas'...")
    cursor.execute("PRAGMA table_info(Vendas)")
    columns = {row[1]: row[2] for row in cursor.fetchall()}
    
    required_columns = {
        'ID': 'INTEGER',
        'Data': 'DATE',
        'Valor': 'REAL',
        'VeiculoID': 'INTEGER',
        'VendedorID': 'INTEGER',
        'ClienteID': 'INTEGER',
        'RegiaoID': 'INTEGER'
    }
    
    for col, col_type in required_columns.items():
        if col in columns:
            print(f"   ✅ Coluna '{col}' ({col_type}) encontrada")
        else:
            print(f"   ❌ ERRO: Coluna '{col}' NÃO encontrada")
            all_tests_passed = False
    
    # Teste 4: Verificar Foreign Keys
    print("\n🔗 1.4. Verificando Foreign Keys da tabela 'Vendas'...")
    cursor.execute("PRAGMA foreign_key_list(Vendas)")
    fks = cursor.fetchall()
    
    expected_fks = ['Veiculos', 'Vendedores', 'Clientes', 'Regioes']
    found_fks = [fk[2] for fk in fks]
    
    for expected in expected_fks:
        if expected in found_fks:
            print(f"   ✅ Foreign Key para '{expected}' configurada")
        else:
            print(f"   ⚠️  AVISO: Foreign Key para '{expected}' não encontrada")
    
    # Teste 5: Verificar estrutura da tabela Vendedores
    print("\n👔 1.5. Verificando estrutura da tabela 'Vendedores'...")
    cursor.execute("PRAGMA table_info(Vendedores)")
    columns = {row[1]: row[2] for row in cursor.fetchall()}
    
    required_columns = {
        'ID': 'INTEGER',
        'Nome': 'TEXT',
        'RegiaoID': 'INTEGER'
    }
    
    for col, col_type in required_columns.items():
        if col in columns:
            print(f"   ✅ Coluna '{col}' ({col_type}) encontrada")
        else:
            print(f"   ❌ ERRO: Coluna '{col}' NÃO encontrada")
            all_tests_passed = False
    
    # Teste 6: Verificar estrutura da tabela Clientes
    print("\n👥 1.6. Verificando estrutura da tabela 'Clientes'...")
    cursor.execute("PRAGMA table_info(Clientes)")
    columns = {row[1]: row[2] for row in cursor.fetchall()}
    
    required_columns = {
        'ID': 'INTEGER',
        'Nome': 'TEXT',
        'Tipo': 'TEXT'
    }
    
    for col, col_type in required_columns.items():
        if col in columns:
            print(f"   ✅ Coluna '{col}' ({col_type}) encontrada")
        else:
            print(f"   ❌ ERRO: Coluna '{col}' NÃO encontrada")
            all_tests_passed = False
    
    # Teste 7: Verificar estrutura da tabela Regioes
    print("\n🌎 1.7. Verificando estrutura da tabela 'Regioes'...")
    cursor.execute("PRAGMA table_info(Regioes)")
    columns = {row[1]: row[2] for row in cursor.fetchall()}
    
    required_columns = {
        'ID': 'INTEGER',
        'Nome': 'TEXT',
        'Estado': 'TEXT'
    }
    
    for col, col_type in required_columns.items():
        if col in columns:
            print(f"   ✅ Coluna '{col}' ({col_type}) encontrada")
        else:
            print(f"   ❌ ERRO: Coluna '{col}' NÃO encontrada")
            all_tests_passed = False
    
    # Teste 8: Verificar se há dados nas tabelas
    print("\n📊 1.8. Verificando presença de dados...")
    
    for table in required_tables:
        cursor.execute(f"SELECT COUNT(*) FROM {table}")
        count = cursor.fetchone()[0]
        if count > 0:
            print(f"   ✅ Tabela '{table}' contém {count} registros")
        else:
            print(f"   ⚠️  AVISO: Tabela '{table}' está vazia")
    
    conn.close()
    
    # Resultado final
    print("\n" + "=" * 80)
    if all_tests_passed:
        print("✅ RESULTADO: TODOS OS TESTES DE ESTRUTURA PASSARAM")
        print("=" * 80)
        return 0
    else:
        print("❌ RESULTADO: ALGUNS TESTES FALHARAM")
        print("=" * 80)
        return 1

if __name__ == "__main__":
    sys.exit(test_database_structure())
