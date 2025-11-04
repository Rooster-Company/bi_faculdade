"""
Script para criar banco de dados SQLite de exemplo
Use este script se não conseguir converter o Access
"""
import sqlite3
import random
from datetime import datetime, timedelta

def create_sample_database():
    """Cria banco de dados SQLite com dados de exemplo"""
    
    conn = sqlite3.connect('vendas.db')
    cursor = conn.cursor()
    
    # Criar tabelas
    print("Criando tabelas...")
    
    # Tabela Regiões
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS Regioes (
        ID INTEGER PRIMARY KEY AUTOINCREMENT,
        Nome TEXT NOT NULL,
        Estado TEXT NOT NULL
    )
    ''')
    
    # Tabela Vendedores
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS Vendedores (
        ID INTEGER PRIMARY KEY AUTOINCREMENT,
        Nome TEXT NOT NULL,
        RegiaoID INTEGER,
        FOREIGN KEY (RegiaoID) REFERENCES Regioes(ID)
    )
    ''')
    
    # Tabela Clientes
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS Clientes (
        ID INTEGER PRIMARY KEY AUTOINCREMENT,
        Nome TEXT NOT NULL,
        Tipo TEXT CHECK(Tipo IN ('Pessoa Física', 'Pessoa Jurídica'))
    )
    ''')
    
    # Tabela Veículos
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS Veiculos (
        ID INTEGER PRIMARY KEY AUTOINCREMENT,
        Modelo TEXT NOT NULL,
        Marca TEXT NOT NULL,
        Categoria TEXT NOT NULL,
        Cor TEXT NOT NULL,
        PrecoUnitario REAL NOT NULL
    )
    ''')
    
    # Tabela Vendas
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS Vendas (
        ID INTEGER PRIMARY KEY AUTOINCREMENT,
        Data DATE NOT NULL,
        Valor REAL NOT NULL,
        VeiculoID INTEGER,
        VendedorID INTEGER,
        ClienteID INTEGER,
        RegiaoID INTEGER,
        FOREIGN KEY (VeiculoID) REFERENCES Veiculos(ID),
        FOREIGN KEY (VendedorID) REFERENCES Vendedores(ID),
        FOREIGN KEY (ClienteID) REFERENCES Clientes(ID),
        FOREIGN KEY (RegiaoID) REFERENCES Regioes(ID)
    )
    ''')
    
    print("Inserindo dados de exemplo...")
    
    # Regiões
    regioes = [
        ('Sul', 'RS'), ('Sul', 'SC'), ('Sul', 'PR'),
        ('Sudeste', 'SP'), ('Sudeste', 'RJ'), ('Sudeste', 'MG'),
        ('Centro-Oeste', 'GO'), ('Centro-Oeste', 'MT'),
        ('Nordeste', 'BA'), ('Nordeste', 'PE'),
        ('Norte', 'AM'), ('Norte', 'PA')
    ]
    cursor.executemany('INSERT INTO Regioes (Nome, Estado) VALUES (?, ?)', regioes)
    
    # Vendedores
    vendedores = [
        'João Silva', 'Maria Santos', 'Pedro Oliveira', 'Ana Costa',
        'Carlos Souza', 'Juliana Lima', 'Roberto Ferreira', 'Patricia Alves',
        'Fernando Rodrigues', 'Beatriz Martins', 'Lucas Pereira', 'Camila Ribeiro'
    ]
    for vendedor in vendedores:
        regiao_id = random.randint(1, 12)
        cursor.execute('INSERT INTO Vendedores (Nome, RegiaoID) VALUES (?, ?)', 
                      (vendedor, regiao_id))
    
    # Clientes
    clientes_pf = [
        'José da Silva', 'Maria Oliveira', 'Antonio Santos', 'Francisca Costa',
        'Paulo Souza', 'Ana Paula Lima', 'Marcos Ferreira', 'Juliana Alves'
    ]
    clientes_pj = [
        'Tech Solutions Ltda', 'Transportadora ABC', 'Comércio XYZ S/A',
        'Indústria Nacional', 'Serviços Premium', 'Logística Express'
    ]
    
    for cliente in clientes_pf:
        cursor.execute('INSERT INTO Clientes (Nome, Tipo) VALUES (?, ?)', 
                      (cliente, 'Pessoa Física'))
    
    for cliente in clientes_pj:
        cursor.execute('INSERT INTO Clientes (Nome, Tipo) VALUES (?, ?)', 
                      (cliente, 'Pessoa Jurídica'))
    
    # Veículos
    marcas = ['Toyota', 'Volkswagen', 'Fiat', 'Chevrolet', 'Honda', 'Hyundai', 'Ford', 'Nissan']
    categorias = ['SUV', 'Sedan', 'Hatch', 'Pickup', 'Minivan']
    cores = ['Preto', 'Branco', 'Prata', 'Vermelho', 'Azul', 'Cinza']
    
    veiculos = []
    for marca in marcas:
        for i in range(1, 6):  # 5 modelos por marca
            modelo = f'{marca} Modelo {i}'
            categoria = random.choice(categorias)
            cor = random.choice(cores)
            preco = random.uniform(50000, 200000)
            veiculos.append((modelo, marca, categoria, cor, preco))
    
    cursor.executemany('''
        INSERT INTO Veiculos (Modelo, Marca, Categoria, Cor, PrecoUnitario) 
        VALUES (?, ?, ?, ?, ?)
    ''', veiculos)
    
    # Vendas - gerar para 2020-2024
    print("Gerando vendas...")
    vendas = []
    
    for ano in range(2020, 2025):
        # Gerar entre 800 e 1200 vendas por ano
        num_vendas = random.randint(800, 1200)
        
        for _ in range(num_vendas):
            # Data aleatória no ano
            start_date = datetime(ano, 1, 1)
            end_date = datetime(ano, 12, 31)
            days_between = (end_date - start_date).days
            random_days = random.randint(0, days_between)
            data_venda = start_date + timedelta(days=random_days)
            
            # IDs aleatórios
            veiculo_id = random.randint(1, len(veiculos))
            vendedor_id = random.randint(1, len(vendedores))
            cliente_id = random.randint(1, len(clientes_pf) + len(clientes_pj))
            regiao_id = random.randint(1, 12)
            
            # Buscar preço do veículo
            cursor.execute('SELECT PrecoUnitario FROM Veiculos WHERE ID = ?', (veiculo_id,))
            preco = cursor.fetchone()[0]
            
            # Adicionar variação no valor (desconto ou acréscimo)
            valor = preco * random.uniform(0.9, 1.1)
            
            vendas.append((
                data_venda.strftime('%Y-%m-%d'),
                valor,
                veiculo_id,
                vendedor_id,
                cliente_id,
                regiao_id
            ))
    
    cursor.executemany('''
        INSERT INTO Vendas (Data, Valor, VeiculoID, VendedorID, ClienteID, RegiaoID)
        VALUES (?, ?, ?, ?, ?, ?)
    ''', vendas)
    
    conn.commit()
    
    # Estatísticas
    cursor.execute('SELECT COUNT(*) FROM Vendas')
    total_vendas = cursor.fetchone()[0]
    
    cursor.execute('SELECT SUM(Valor) FROM Vendas')
    faturamento_total = cursor.fetchone()[0]
    
    print(f"\n✅ Banco de dados criado com sucesso!")
    print(f"📊 Total de vendas: {total_vendas}")
    print(f"💰 Faturamento total: R$ {faturamento_total:,.2f}")
    
    conn.close()

if __name__ == "__main__":
    create_sample_database()
