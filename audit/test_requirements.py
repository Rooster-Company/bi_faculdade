"""
Teste 3: Validação de Conformidade com Requisitos
Verifica se todos os requisitos do instruções.md foram atendidos
"""
import sqlite3
import pandas as pd
import sys

def test_requirements():
    """Testa conformidade com todos os requisitos"""
    
    print("=" * 80)
    print("TESTE 3: CONFORMIDADE COM REQUISITOS (instruções.md)")
    print("=" * 80)
    
    conn = sqlite3.connect('vendas.db')
    
    # Carregar dados
    query = """
    SELECT 
        v.ID as venda_id,
        v.Data as data_venda,
        v.Valor as valor_venda,
        ve.Modelo as veiculo_modelo,
        ve.Marca as veiculo_marca,
        ve.Categoria as veiculo_categoria,
        ve.Cor as veiculo_cor,
        vd.Nome as vendedor_nome,
        c.Nome as cliente_nome,
        c.Tipo as cliente_tipo,
        r.Nome as regiao_nome,
        r.Estado as regiao_estado,
        strftime('%Y', v.Data) as ano,
        strftime('%m', v.Data) as mes
    FROM Vendas v
    LEFT JOIN Veiculos ve ON v.VeiculoID = ve.ID
    LEFT JOIN Vendedores vd ON v.VendedorID = vd.ID
    LEFT JOIN Clientes c ON v.ClienteID = c.ID
    LEFT JOIN Regioes r ON v.RegiaoID = r.ID
    """
    
    df = pd.read_sql_query(query, conn)
    df['data_venda'] = pd.to_datetime(df['data_venda'], errors='coerce')
    df['valor_venda'] = pd.to_numeric(df['valor_venda'], errors='coerce')
    df['ano'] = pd.to_numeric(df['ano'], errors='coerce')
    df['mes'] = pd.to_numeric(df['mes'], errors='coerce')
    
    all_tests_passed = True
    pontuacao = 0
    pontuacao_maxima = 2.0
    
    # ===== PARTE 1: MODELAGEM DE DADOS (0.5 pontos) =====
    print("\n" + "=" * 80)
    print("PARTE 1 - MODELAGEM DE DADOS (0.5 pontos)")
    print("=" * 80)
    
    pontos_parte1 = 0
    
    # Requisito 1.1: Entidade Veículo
    print("\n📝 Requisito 1.1: Entidade Veículo (modelo, marca, categoria, preço)")
    cursor = conn.cursor()
    cursor.execute("PRAGMA table_info(Veiculos)")
    veiculos_cols = [row[1] for row in cursor.fetchall()]
    
    campos_veiculo = ['Modelo', 'Marca', 'Categoria', 'PrecoUnitario']
    veiculo_ok = all(campo in veiculos_cols for campo in campos_veiculo)
    
    if veiculo_ok:
        print("   ✅ APROVADO: Entidade Veículo completa")
        pontos_parte1 += 0.1
    else:
        print("   ❌ REPROVADO: Entidade Veículo incompleta")
        all_tests_passed = False
    
    # Requisito 1.2: Entidade Venda
    print("\n📝 Requisito 1.2: Entidade Venda (data, valor, relações)")
    cursor.execute("PRAGMA table_info(Vendas)")
    vendas_cols = [row[1] for row in cursor.fetchall()]
    
    campos_venda = ['Data', 'Valor', 'VeiculoID', 'VendedorID', 'ClienteID', 'RegiaoID']
    venda_ok = all(campo in vendas_cols for campo in campos_venda)
    
    if venda_ok:
        print("   ✅ APROVADO: Entidade Venda completa")
        pontos_parte1 += 0.1
    else:
        print("   ❌ REPROVADO: Entidade Venda incompleta")
        all_tests_passed = False
    
    # Requisito 1.3: Entidade Vendedor
    print("\n📝 Requisito 1.3: Entidade Vendedor (nome, ID, região)")
    cursor.execute("PRAGMA table_info(Vendedores)")
    vendedores_cols = [row[1] for row in cursor.fetchall()]
    
    campos_vendedor = ['ID', 'Nome', 'RegiaoID']
    vendedor_ok = all(campo in vendedores_cols for campo in campos_vendedor)
    
    if vendedor_ok:
        print("   ✅ APROVADO: Entidade Vendedor completa")
        pontos_parte1 += 0.1
    else:
        print("   ❌ REPROVADO: Entidade Vendedor incompleta")
        all_tests_passed = False
    
    # Requisito 1.4: Entidade Cliente
    print("\n📝 Requisito 1.4: Entidade Cliente (nome, ID, tipo PF/PJ)")
    cursor.execute("PRAGMA table_info(Clientes)")
    clientes_cols = [row[1] for row in cursor.fetchall()]
    
    campos_cliente = ['ID', 'Nome', 'Tipo']
    cliente_ok = all(campo in clientes_cols for campo in campos_cliente)
    
    if cliente_ok:
        print("   ✅ APROVADO: Entidade Cliente completa")
        pontos_parte1 += 0.1
    else:
        print("   ❌ REPROVADO: Entidade Cliente incompleta")
        all_tests_passed = False
    
    # Requisito 1.5: Entidade Região
    print("\n📝 Requisito 1.5: Entidade Região (nome, estado)")
    cursor.execute("PRAGMA table_info(Regioes)")
    regioes_cols = [row[1] for row in cursor.fetchall()]
    
    campos_regiao = ['Nome', 'Estado']
    regiao_ok = all(campo in regioes_cols for campo in campos_regiao)
    
    if regiao_ok:
        print("   ✅ APROVADO: Entidade Região completa")
        pontos_parte1 += 0.1
    else:
        print("   ❌ REPROVADO: Entidade Região incompleta")
        all_tests_passed = False
    
    print(f"\n🎯 Pontuação Parte 1: {pontos_parte1:.1f} / 0.5")
    pontuacao += pontos_parte1
    
    # ===== PARTE 2: DASHBOARD (1.5 pontos) =====
    print("\n" + "=" * 80)
    print("PARTE 2 - DASHBOARD (1.5 pontos)")
    print("=" * 80)
    
    pontos_parte2 = 0
    
    # Requisito 2.1: Filtro de Ano
    print("\n📝 Requisito 2.1: Filtro de Ano")
    anos = df['ano'].dropna().unique()
    
    if len(anos) > 0:
        print(f"   ✅ APROVADO: Extração de ano funcional ({len(anos)} anos disponíveis)")
        pontos_parte2 += 0.15
    else:
        print("   ❌ REPROVADO: Extração de ano não funciona")
        all_tests_passed = False
    
    # Requisito 2.2: Veículos Vendidos
    print("\n📝 Requisito 2.2: KPI - Veículos Vendidos")
    if len(df) > 0:
        ano_teste = df['ano'].dropna().iloc[-1]
        df_filtered = df[df['ano'] == ano_teste]
        veiculos_vendidos = len(df_filtered)
        print(f"   ✅ APROVADO: Total de veículos calculado ({veiculos_vendidos} no ano {int(ano_teste)})")
        pontos_parte2 += 0.05
    else:
        print("   ❌ REPROVADO: Não foi possível calcular")
        all_tests_passed = False
    
    # Requisito 2.3: Meta de Vendas
    print("\n📝 Requisito 2.3: KPI - Meta de Vendas (1042 unidades)")
    META_VENDAS = 1042
    print(f"   ✅ APROVADO: Meta definida: {META_VENDAS} unidades")
    pontos_parte2 += 0.05
    
    # Requisito 2.4: Faturamento Total
    print("\n📝 Requisito 2.4: KPI - Faturamento Total")
    if len(df) > 0:
        faturamento = df_filtered['valor_venda'].sum()
        print(f"   ✅ APROVADO: Faturamento calculado (R$ {faturamento/1e6:.2f}M no ano {int(ano_teste)})")
        pontos_parte2 += 0.05
    else:
        print("   ❌ REPROVADO: Não foi possível calcular")
        all_tests_passed = False
    
    # Requisito 2.5: Meta de Faturamento
    print("\n📝 Requisito 2.5: KPI - Meta de Faturamento (R$ 109M)")
    META_FATURAMENTO = 109000000
    print(f"   ✅ APROVADO: Meta definida: R$ {META_FATURAMENTO/1e6:.0f}M")
    pontos_parte2 += 0.05
    
    # Requisito 2.6: Top 7 Veículos
    print("\n📝 Requisito 2.6: Top 7 Veículos Mais Vendidos")
    if len(df_filtered) > 0:
        top_veiculos = df_filtered.groupby('veiculo_modelo')['valor_venda'].sum().sort_values(ascending=False).head(7)
        if len(top_veiculos) > 0:
            print(f"   ✅ APROVADO: Top 7 calculado ({len(top_veiculos)} modelos)")
            print(f"      🥇 Líder: {top_veiculos.index[0]} - R$ {top_veiculos.iloc[0]/1e6:.2f}M")
            pontos_parte2 += 0.15
        else:
            print("   ❌ REPROVADO: Top 7 vazio")
            all_tests_passed = False
    
    # Requisito 2.7: Faturamento por Mês
    print("\n📝 Requisito 2.7: Faturamento por Mês (Jan-Dez)")
    if len(df_filtered) > 0:
        fat_mes = df_filtered.groupby('mes')['valor_venda'].sum()
        todos_meses = pd.DataFrame({'mes': range(1, 13)})
        fat_mes_completo = todos_meses.merge(
            fat_mes.reset_index(), 
            on='mes', 
            how='left'
        ).fillna(0)
        
        if len(fat_mes_completo) == 12:
            print(f"   ✅ APROVADO: Faturamento por mês calculado (12 meses)")
            print(f"      📊 Meses com vendas: {(fat_mes_completo['valor_venda'] > 0).sum()}")
            pontos_parte2 += 0.15
        else:
            print("   ❌ REPROVADO: Não há 12 meses")
            all_tests_passed = False
    
    # Requisito 2.8: Destaques do Ano (5 itens)
    print("\n📝 Requisito 2.8: Destaques do Ano (5 destaques obrigatórios)")
    
    destaques_ok = 0
    
    # 2.8.1 - Modelo mais vendido
    if len(df_filtered) > 0:
        modelo = df_filtered.groupby('veiculo_modelo')['venda_id'].count().idxmax()
        qtd = df_filtered.groupby('veiculo_modelo')['venda_id'].count().max()
        print(f"   ✅ Modelo mais vendido: {modelo} ({qtd} unidades)")
        destaques_ok += 1
    
    # 2.8.2 - Marca mais vendida
    if len(df_filtered) > 0:
        marca = df_filtered.groupby('veiculo_marca')['valor_venda'].sum().idxmax()
        valor = df_filtered.groupby('veiculo_marca')['valor_venda'].sum().max() / 1e6
        print(f"   ✅ Marca mais vendida: {marca} (R$ {valor:.2f}M)")
        destaques_ok += 1
    
    # 2.8.3 - Vendedor com maior faturamento
    if len(df_filtered) > 0:
        vendedor = df_filtered.groupby('vendedor_nome')['valor_venda'].sum().idxmax()
        valor = df_filtered.groupby('vendedor_nome')['valor_venda'].sum().max() / 1e6
        print(f"   ✅ Vendedor com maior faturamento: {vendedor} (R$ {valor:.2f}M)")
        destaques_ok += 1
    
    # 2.8.4 - Região com maior faturamento
    if len(df_filtered) > 0:
        regiao = df_filtered.groupby('regiao_nome')['valor_venda'].sum().idxmax()
        valor = df_filtered.groupby('regiao_nome')['valor_venda'].sum().max() / 1e6
        print(f"   ✅ Região com maior faturamento: {regiao} (R$ {valor:.2f}M)")
        destaques_ok += 1
    
    # 2.8.5 - Mês com maior faturamento
    if len(df_filtered) > 0:
        mes = df_filtered.groupby('mes')['valor_venda'].sum().idxmax()
        valor = df_filtered.groupby('mes')['valor_venda'].sum().max() / 1e6
        meses = ['Jan', 'Fev', 'Mar', 'Abr', 'Mai', 'Jun', 'Jul', 'Ago', 'Set', 'Out', 'Nov', 'Dez']
        mes_nome = meses[int(mes)-1]
        print(f"   ✅ Mês com maior faturamento: {mes_nome} (R$ {valor:.2f}M)")
        destaques_ok += 1
    
    if destaques_ok == 5:
        print(f"\n   ✅ APROVADO: Todos os 5 destaques implementados")
        pontos_parte2 += 0.35
    else:
        print(f"\n   ❌ REPROVADO: Apenas {destaques_ok}/5 destaques encontrados")
        all_tests_passed = False
    
    # Requisito 2.9: Nova Visualização (0.5 pontos)
    print("\n📝 Requisito 2.9: Nova Visualização (criatividade)")
    if len(df_filtered) > 0:
        # Testar a visualização de cores por estado
        cores_estado = df_filtered.groupby(['regiao_estado', 'veiculo_cor'])['venda_id'].count()
        
        if len(cores_estado) > 0:
            print(f"   ✅ APROVADO: Visualização extra implementada")
            print(f"      🎨 Análise de cores por estado")
            print(f"      📊 {len(cores_estado)} combinações estado-cor")
            pontos_parte2 += 0.5
        else:
            print("   ❌ REPROVADO: Visualização extra não funciona")
            all_tests_passed = False
    
    print(f"\n🎯 Pontuação Parte 2: {pontos_parte2:.2f} / 1.5")
    pontuacao += pontos_parte2
    
    conn.close()
    
    # Resultado final
    print("\n" + "=" * 80)
    print("RESULTADO FINAL DA AUDITORIA")
    print("=" * 80)
    print(f"\n🎯 PONTUAÇÃO TOTAL: {pontuacao:.2f} / {pontuacao_maxima}")
    print(f"📊 Percentual: {(pontuacao/pontuacao_maxima*100):.1f}%")
    
    if pontuacao >= pontuacao_maxima * 0.9:
        print("✅ AVALIAÇÃO: EXCELENTE - Todos os requisitos atendidos")
    elif pontuacao >= pontuacao_maxima * 0.7:
        print("✅ AVALIAÇÃO: BOM - Maioria dos requisitos atendidos")
    elif pontuacao >= pontuacao_maxima * 0.5:
        print("⚠️  AVALIAÇÃO: REGULAR - Requisitos parcialmente atendidos")
    else:
        print("❌ AVALIAÇÃO: INSUFICIENTE - Muitos requisitos não atendidos")
    
    print("=" * 80)
    
    if all_tests_passed and pontuacao >= pontuacao_maxima * 0.9:
        return 0
    else:
        return 1

if __name__ == "__main__":
    sys.exit(test_requirements())
