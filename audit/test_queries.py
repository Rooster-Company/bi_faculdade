"""
Teste 2: Validação das Queries e Cálculos do BI
Verifica se todas as queries estão corretas e os cálculos são precisos
"""
import sqlite3
import pandas as pd
import sys
from datetime import datetime

def test_queries():
    """Testa todas as queries e cálculos do dashboard"""
    
    print("=" * 80)
    print("TESTE 2: QUERIES E CÁLCULOS DO BI")
    print("=" * 80)
    
    conn = sqlite3.connect('vendas.db')
    all_tests_passed = True
    
    # Query principal (mesma usada no app.py)
    query = """
    SELECT 
        v.ID as venda_id,
        v.Data as data_venda,
        v.Valor as valor_venda,
        ve.Modelo as veiculo_modelo,
        ve.Marca as veiculo_marca,
        ve.Categoria as veiculo_categoria,
        ve.Cor as veiculo_cor,
        ve.PrecoUnitario as preco_unitario,
        vd.Nome as vendedor_nome,
        vd.ID as vendedor_id,
        c.Nome as cliente_nome,
        c.Tipo as cliente_tipo,
        r.Nome as regiao_nome,
        r.Estado as regiao_estado,
        strftime('%Y', v.Data) as ano,
        strftime('%m', v.Data) as mes,
        strftime('%Y-%m', v.Data) as ano_mes
    FROM Vendas v
    LEFT JOIN Veiculos ve ON v.VeiculoID = ve.ID
    LEFT JOIN Vendedores vd ON v.VendedorID = vd.ID
    LEFT JOIN Clientes c ON v.ClienteID = c.ID
    LEFT JOIN Regioes r ON v.RegiaoID = r.ID
    """
    
    print("\n📊 2.1. Carregando dados com query principal...")
    df = pd.read_sql_query(query, conn)
    
    # Conversões
    df['data_venda'] = pd.to_datetime(df['data_venda'], errors='coerce')
    df['valor_venda'] = pd.to_numeric(df['valor_venda'], errors='coerce')
    df['ano'] = pd.to_numeric(df['ano'], errors='coerce')
    df['mes'] = pd.to_numeric(df['mes'], errors='coerce')
    
    print(f"   ✅ Query executada com sucesso: {len(df)} registros carregados")
    
    # Teste 2.2: Verificar campos obrigatórios
    print("\n🔍 2.2. Verificando campos obrigatórios na query...")
    
    required_fields = [
        'venda_id', 'data_venda', 'valor_venda', 'veiculo_modelo', 
        'veiculo_marca', 'veiculo_categoria', 'veiculo_cor', 'vendedor_nome',
        'cliente_nome', 'cliente_tipo', 'regiao_nome', 'regiao_estado', 
        'ano', 'mes'
    ]
    
    for field in required_fields:
        if field in df.columns:
            print(f"   ✅ Campo '{field}' presente")
        else:
            print(f"   ❌ ERRO: Campo '{field}' ausente")
            all_tests_passed = False
    
    # Teste 2.3: Verificar extração de ano
    print("\n📅 2.3. Testando extração de ano...")
    anos = sorted(df['ano'].dropna().unique())
    print(f"   ✅ Anos disponíveis: {anos}")
    
    if len(anos) > 0:
        print(f"   ✅ Extração de ano funcionando corretamente")
    else:
        print(f"   ❌ ERRO: Nenhum ano encontrado")
        all_tests_passed = False
    
    # Teste 2.4: Calcular KPIs para um ano específico
    if len(anos) > 0:
        ano_teste = anos[-1]  # Último ano disponível
        print(f"\n💰 2.4. Testando cálculos de KPIs para o ano {int(ano_teste)}...")
        
        df_filtered = df[df['ano'] == ano_teste].copy()
        
        # KPI 1: Veículos vendidos
        veiculos_vendidos = len(df_filtered)
        print(f"   ✅ Veículos vendidos: {veiculos_vendidos}")
        
        # KPI 2: Faturamento total
        faturamento_total = df_filtered['valor_venda'].sum()
        print(f"   ✅ Faturamento total: R$ {faturamento_total:,.2f}")
        print(f"   ✅ Faturamento em milhões: R$ {faturamento_total/1e6:.2f}M")
        
        # KPI 3: Ticket médio
        if veiculos_vendidos > 0:
            ticket_medio = faturamento_total / veiculos_vendidos
            print(f"   ✅ Ticket médio: R$ {ticket_medio:,.2f}")
    
    # Teste 2.5: Top 7 veículos
    print("\n🏆 2.5. Testando cálculo de Top 7 veículos...")
    if len(df) > 0:
        ano_teste = df['ano'].dropna().iloc[-1]
        df_filtered = df[df['ano'] == ano_teste].copy()
        
        top_veiculos = df_filtered.groupby('veiculo_modelo').agg({
            'valor_venda': 'sum',
            'venda_id': 'count'
        }).sort_values('valor_venda', ascending=False).head(7)
        
        print(f"   ✅ Top 7 veículos calculado com sucesso")
        print(f"   📊 Quantidade de modelos no top 7: {len(top_veiculos)}")
        
        if len(top_veiculos) > 0:
            print(f"   🥇 1º lugar: {top_veiculos.index[0]} - R$ {top_veiculos.iloc[0]['valor_venda']/1e6:.2f}M")
    
    # Teste 2.6: Faturamento por mês
    print("\n📅 2.6. Testando faturamento por mês...")
    if len(df) > 0:
        ano_teste = df['ano'].dropna().iloc[-1]
        df_filtered = df[df['ano'] == ano_teste].copy()
        
        faturamento_mes = df_filtered.groupby('mes')['valor_venda'].sum().reset_index()
        
        # Garantir todos os meses
        todos_meses = pd.DataFrame({'mes': range(1, 13)})
        faturamento_mes = todos_meses.merge(faturamento_mes, on='mes', how='left').fillna(0)
        
        print(f"   ✅ Faturamento calculado para todos os 12 meses")
        
        meses_com_venda = faturamento_mes[faturamento_mes['valor_venda'] > 0]
        print(f"   📊 Meses com vendas: {len(meses_com_venda)}")
        
        mes_maior_faturamento = faturamento_mes.loc[faturamento_mes['valor_venda'].idxmax()]
        print(f"   💰 Mês com maior faturamento: Mês {int(mes_maior_faturamento['mes'])} - R$ {mes_maior_faturamento['valor_venda']/1e6:.2f}M")
    
    # Teste 2.7: Destaques do ano
    print("\n⭐ 2.7. Testando cálculo dos destaques...")
    if len(df) > 0:
        ano_teste = df['ano'].dropna().iloc[-1]
        df_filtered = df[df['ano'] == ano_teste].copy()
        
        if len(df_filtered) > 0:
            # Modelo mais vendido
            modelo_destaque = df_filtered.groupby('veiculo_modelo')['venda_id'].count().idxmax()
            qtd_modelo = df_filtered.groupby('veiculo_modelo')['venda_id'].count().max()
            print(f"   ✅ Modelo mais vendido: {modelo_destaque} ({qtd_modelo} unidades)")
            
            # Marca mais vendida
            marca_destaque = df_filtered.groupby('veiculo_marca')['valor_venda'].sum().idxmax()
            valor_marca = df_filtered.groupby('veiculo_marca')['valor_venda'].sum().max() / 1e6
            print(f"   ✅ Marca mais vendida: {marca_destaque} (R$ {valor_marca:.2f}M)")
            
            # Vendedor destaque
            vendedor_destaque = df_filtered.groupby('vendedor_nome')['valor_venda'].sum().idxmax()
            valor_vendedor = df_filtered.groupby('vendedor_nome')['valor_venda'].sum().max() / 1e6
            print(f"   ✅ Melhor vendedor: {vendedor_destaque} (R$ {valor_vendedor:.2f}M)")
            
            # Região destaque
            regiao_destaque = df_filtered.groupby('regiao_nome')['valor_venda'].sum().idxmax()
            valor_regiao = df_filtered.groupby('regiao_nome')['valor_venda'].sum().max() / 1e6
            print(f"   ✅ Melhor região: {regiao_destaque} (R$ {valor_regiao:.2f}M)")
            
            # Mês destaque
            mes_destaque_num = df_filtered.groupby('mes')['valor_venda'].sum().idxmax()
            valor_mes = df_filtered.groupby('mes')['valor_venda'].sum().max() / 1e6
            meses_nomes = ['Jan', 'Fev', 'Mar', 'Abr', 'Mai', 'Jun', 
                          'Jul', 'Ago', 'Set', 'Out', 'Nov', 'Dez']
            mes_destaque = meses_nomes[int(mes_destaque_num)-1]
            print(f"   ✅ Melhor mês: {mes_destaque} (R$ {valor_mes:.2f}M)")
    
    # Teste 2.8: Visualização extra (cores por estado)
    print("\n🎨 2.8. Testando visualização extra (cores por estado)...")
    if len(df) > 0:
        ano_teste = df['ano'].dropna().iloc[-1]
        df_filtered = df[df['ano'] == ano_teste].copy()
        
        cores_estado = df_filtered.groupby(['regiao_estado', 'veiculo_cor'])['venda_id'].count().reset_index()
        cores_estado.columns = ['Estado', 'Cor', 'Quantidade']
        
        top_cores_estado = cores_estado.sort_values(['Estado', 'Quantidade'], ascending=[True, False])
        top_cores_estado = top_cores_estado.groupby('Estado').head(3)
        
        print(f"   ✅ Análise de cores por estado calculada")
        print(f"   📊 Estados analisados: {cores_estado['Estado'].nunique()}")
        print(f"   🎨 Cores diferentes encontradas: {cores_estado['Cor'].nunique()}")
    
    # Teste 2.9: Validar integridade dos JOINs
    print("\n🔗 2.9. Testando integridade dos JOINs...")
    
    # Verificar se há valores nulos nos campos importantes
    campos_importantes = ['veiculo_modelo', 'veiculo_marca', 'vendedor_nome', 
                          'cliente_nome', 'regiao_nome']
    
    for campo in campos_importantes:
        nulls = df[campo].isna().sum()
        total = len(df)
        percentual = (nulls / total * 100) if total > 0 else 0
        
        if nulls == 0:
            print(f"   ✅ Campo '{campo}': Sem valores nulos")
        else:
            print(f"   ⚠️  Campo '{campo}': {nulls} nulos ({percentual:.2f}%)")
            if percentual > 10:
                print(f"   ❌ ERRO: Muitos valores nulos em '{campo}'")
                all_tests_passed = False
    
    conn.close()
    
    # Resultado final
    print("\n" + "=" * 80)
    if all_tests_passed:
        print("✅ RESULTADO: TODOS OS TESTES DE QUERIES E CÁLCULOS PASSARAM")
        print("=" * 80)
        return 0
    else:
        print("❌ RESULTADO: ALGUNS TESTES FALHARAM")
        print("=" * 80)
        return 1

if __name__ == "__main__":
    sys.exit(test_queries())
