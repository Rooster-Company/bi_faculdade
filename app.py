"""
Dashboard BI - Sistema de Vendas de Veículos
Trabalho de Faculdade
"""
import streamlit as st
import pandas as pd
import sqlite3
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime

# Configuração da página
st.set_page_config(
    page_title="BI Vendas de Veículos",
    page_icon="🚗",
    layout="wide",
    initial_sidebar_state="expanded"
)

# CSS customizado
st.markdown("""
    <style>
    .main {
        background-color: #0e1117;
    }
    
    /* Estilo para métricas */
    div[data-testid="stMetricValue"] {
        font-size: 2.2rem;
        font-weight: 700;
        color: #ffffff;
    }
    
    div[data-testid="stMetricLabel"] {
        font-size: 1rem;
        font-weight: 500;
        color: #ffffff;
        opacity: 0.9;
    }
    
    div[data-testid="stMetricDelta"] {
        font-size: 0.9rem;
        font-weight: 600;
    }
    
    /* Cards coloridos para cada métrica */
    [data-testid="column"]:nth-of-type(1) [data-testid="stMetric"] {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 25px 20px;
        border-radius: 15px;
        box-shadow: 0 8px 16px rgba(102, 126, 234, 0.3);
        border: 1px solid rgba(255, 255, 255, 0.1);
    }
    
    [data-testid="column"]:nth-of-type(2) [data-testid="stMetric"] {
        background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
        padding: 25px 20px;
        border-radius: 15px;
        box-shadow: 0 8px 16px rgba(240, 147, 251, 0.3);
        border: 1px solid rgba(255, 255, 255, 0.1);
    }
    
    [data-testid="column"]:nth-of-type(3) [data-testid="stMetric"] {
        background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);
        padding: 25px 20px;
        border-radius: 15px;
        box-shadow: 0 8px 16px rgba(79, 172, 254, 0.3);
        border: 1px solid rgba(255, 255, 255, 0.1);
    }
    
    [data-testid="column"]:nth-of-type(4) [data-testid="stMetric"] {
        background: linear-gradient(135deg, #43e97b 0%, #38f9d7 100%);
        padding: 25px 20px;
        border-radius: 15px;
        box-shadow: 0 8px 16px rgba(67, 233, 123, 0.3);
        border: 1px solid rgba(255, 255, 255, 0.1);
    }
    
    /* Títulos */
    h1 {
        color: #ffffff;
        font-weight: 700;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
    }
    
    h2, h3 {
        color: #ffffff;
        font-weight: 600;
    }
    
    /* Cards de informação */
    .stAlert {
        background-color: rgba(255, 255, 255, 0.05);
        border-radius: 10px;
        border: 1px solid rgba(255, 255, 255, 0.1);
        backdrop-filter: blur(10px);
    }
    
    /* Sidebar */
    section[data-testid="stSidebar"] {
        background: linear-gradient(180deg, #1e3c72 0%, #2a5298 100%);
    }
    
    section[data-testid="stSidebar"] h1,
    section[data-testid="stSidebar"] h2,
    section[data-testid="stSidebar"] h3,
    section[data-testid="stSidebar"] label {
        color: #ffffff !important;
    }
    
    /* Gráficos */
    .js-plotly-plot {
        background-color: rgba(255, 255, 255, 0.05);
        border-radius: 15px;
        padding: 15px;
        border: 1px solid rgba(255, 255, 255, 0.1);
    }
    
    /* Tabelas */
    [data-testid="stDataFrame"] {
        background-color: rgba(255, 255, 255, 0.05);
        border-radius: 10px;
        border: 1px solid rgba(255, 255, 255, 0.1);
    }
    </style>
""", unsafe_allow_html=True)

# Funções de banco de dados
@st.cache_resource
def get_connection():
    """Cria conexão com o banco SQLite"""
    return sqlite3.connect('vendas.db', check_same_thread=False)

@st.cache_data(ttl=600)
def load_data():
    """Carrega dados do banco"""
    conn = get_connection()
    
    # Query principal com todos os dados necessários
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
    
    df = pd.read_sql_query(query, conn)
    
    # Conversões de tipo
    df['data_venda'] = pd.to_datetime(df['data_venda'], errors='coerce')
    df['valor_venda'] = pd.to_numeric(df['valor_venda'], errors='coerce')
    df['preco_unitario'] = pd.to_numeric(df['preco_unitario'], errors='coerce')
    df['ano'] = pd.to_numeric(df['ano'], errors='coerce')
    df['mes'] = pd.to_numeric(df['mes'], errors='coerce')
    
    return df

# Carregar dados
try:
    df = load_data()
except Exception as e:
    st.error(f"❌ Erro ao carregar dados: {e}")
    st.info("📝 Execute primeiro o script convert_db.py para criar o banco SQLite")
    st.stop()

# Sidebar - Filtros
st.sidebar.title("🔍 Filtros")
st.sidebar.markdown("---")

# Filtro de Ano
anos_disponiveis = sorted(df['ano'].dropna().unique())
if len(anos_disponiveis) > 0:
    ano_selecionado = st.sidebar.selectbox(
        "📅 Selecione o Ano:",
        options=anos_disponiveis,
        index=len(anos_disponiveis)-1
    )
else:
    st.error("Nenhum dado disponível")
    st.stop()

# Filtros adicionais
st.sidebar.markdown("### Filtros Adicionais")
regioes = ["Todas"] + sorted(df['regiao_nome'].dropna().unique().tolist())
regiao_selecionada = st.sidebar.selectbox("🌎 Região:", regioes)

marcas = ["Todas"] + sorted(df['veiculo_marca'].dropna().unique().tolist())
marca_selecionada = st.sidebar.selectbox("🚗 Marca:", marcas)

# Aplicar filtros
df_filtered = df[df['ano'] == ano_selecionado].copy()

if regiao_selecionada != "Todas":
    df_filtered = df_filtered[df_filtered['regiao_nome'] == regiao_selecionada]

if marca_selecionada != "Todas":
    df_filtered = df_filtered[df_filtered['veiculo_marca'] == marca_selecionada]

# Cabeçalho
st.title("🚗 Dashboard de Vendas de Veículos")
st.markdown(f"### Análise do Ano: **{int(ano_selecionado)}**")
st.markdown("---")

# Metas realistas baseadas nos dados históricos
# Calculadas com base na média dos anos anteriores + 10% de crescimento
METAS_POR_ANO = {
    2020: {'vendas': 900, 'faturamento': 105000000},    # R$ 105M - ano inicial
    2021: {'vendas': 1000, 'faturamento': 115000000},   # R$ 115M - crescimento de ~10%
    2022: {'vendas': 1050, 'faturamento': 120000000},   # R$ 120M - crescimento incremental
    2023: {'vendas': 1100, 'faturamento': 130000000},   # R$ 130M - meta desafiadora
    2024: {'vendas': 1000, 'faturamento': 115000000},   # R$ 115M - ajuste realista
}

# Obter metas do ano selecionado (usa 2024 como padrão se ano não estiver definido)
ano_int = int(ano_selecionado)
metas_ano = METAS_POR_ANO.get(ano_int, {'vendas': 1000, 'faturamento': 115000000})
META_VENDAS = metas_ano['vendas']
META_FATURAMENTO = metas_ano['faturamento']

# KPIs Principais
col1, col2, col3, col4 = st.columns(4)

with col1:
    veiculos_vendidos = len(df_filtered)
    delta_vendas = veiculos_vendidos - META_VENDAS
    st.metric(
        label="🚗 Veículos Vendidos",
        value=f"{veiculos_vendidos:,}",
        delta=f"{delta_vendas:+,} vs meta ({META_VENDAS:,})",
        delta_color="normal"
    )

with col2:
    percentual_meta = (veiculos_vendidos / META_VENDAS * 100) if META_VENDAS > 0 else 0
    delta_perc_vendas = percentual_meta - 100
    st.metric(
        label="📊 % da Meta de Vendas",
        value=f"{percentual_meta:.1f}%",
        delta=f"{delta_perc_vendas:+.1f}%",
        delta_color="normal"
    )

with col3:
    faturamento_total = df_filtered['valor_venda'].sum()
    delta_faturamento = faturamento_total - META_FATURAMENTO
    st.metric(
        label="💰 Faturamento Total",
        value=f"R$ {faturamento_total/1e6:.1f}M",
        delta=f"{delta_faturamento/1e6:.1f}M vs meta (R$ {META_FATURAMENTO/1e6:.0f}M)",
        delta_color="normal"
    )

with col4:
    percentual_fat = (faturamento_total / META_FATURAMENTO * 100) if META_FATURAMENTO > 0 else 0
    delta_perc_fat = percentual_fat - 100
    st.metric(
        label="📈 % da Meta de Faturamento",
        value=f"{percentual_fat:.1f}%",
        delta=f"{delta_perc_fat:+.1f}%",
        delta_color="normal"
    )

st.markdown("---")

# Layout com 2 colunas
col_left, col_right = st.columns([1, 1])

with col_left:
    st.subheader("🏆 Top 7 Veículos Mais Vendidos")
    
    top_veiculos = df_filtered.groupby('veiculo_modelo').agg({
        'valor_venda': 'sum',
        'venda_id': 'count'
    }).sort_values('valor_venda', ascending=False).head(7)
    
    top_veiculos.columns = ['Faturamento', 'Quantidade']
    top_veiculos['Faturamento_M'] = top_veiculos['Faturamento'] / 1e6
    
    fig_top = px.bar(
        top_veiculos.reset_index(),
        x='Faturamento_M',
        y='veiculo_modelo',
        orientation='h',
        labels={'Faturamento_M': 'Faturamento (R$ Milhões)', 'veiculo_modelo': 'Modelo'},
        title='',
        color='Faturamento_M',
        color_continuous_scale='Viridis'
    )
    fig_top.update_layout(
        height=400, 
        showlegend=False,
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(color='white', size=12),
        xaxis=dict(gridcolor='rgba(255,255,255,0.1)', showgrid=True),
        yaxis=dict(gridcolor='rgba(255,255,255,0.1)', showgrid=False),
        margin=dict(l=10, r=10, t=10, b=10)
    )
    st.plotly_chart(fig_top, width='stretch')

with col_right:
    st.subheader("📅 Faturamento por Mês")
    
    faturamento_mes = df_filtered.groupby('mes')['valor_venda'].sum().reset_index()
    faturamento_mes['Faturamento_M'] = faturamento_mes['valor_venda'] / 1e6
    
    # Garantir todos os meses
    todos_meses = pd.DataFrame({'mes': range(1, 13)})
    faturamento_mes = todos_meses.merge(faturamento_mes, on='mes', how='left').fillna(0)
    
    meses_nomes = ['Jan', 'Fev', 'Mar', 'Abr', 'Mai', 'Jun', 
                   'Jul', 'Ago', 'Set', 'Out', 'Nov', 'Dez']
    faturamento_mes['mes_nome'] = faturamento_mes['mes'].apply(lambda x: meses_nomes[int(x)-1])
    
    fig_mes = px.bar(
        faturamento_mes,
        x='mes_nome',
        y='Faturamento_M',
        labels={'Faturamento_M': 'Faturamento (R$ Milhões)', 'mes_nome': 'Mês'},
        title='',
        color='Faturamento_M',
        color_continuous_scale='Plasma'
    )
    fig_mes.update_layout(
        height=400, 
        showlegend=False,
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(color='white', size=12),
        xaxis=dict(gridcolor='rgba(255,255,255,0.1)', showgrid=False),
        yaxis=dict(gridcolor='rgba(255,255,255,0.1)', showgrid=True),
        margin=dict(l=10, r=10, t=10, b=10)
    )
    st.plotly_chart(fig_mes, width='stretch')

st.markdown("---")

# Destaques do Ano
st.subheader("⭐ Destaques do Ano")

# Calcular destaques
modelo_destaque = df_filtered.groupby('veiculo_modelo')['venda_id'].count().idxmax() if len(df_filtered) > 0 else "N/A"
qtd_modelo = df_filtered.groupby('veiculo_modelo')['venda_id'].count().max() if len(df_filtered) > 0 else 0

marca_destaque = df_filtered.groupby('veiculo_marca')['valor_venda'].sum().idxmax() if len(df_filtered) > 0 else "N/A"
valor_marca = df_filtered.groupby('veiculo_marca')['valor_venda'].sum().max() / 1e6 if len(df_filtered) > 0 else 0

vendedor_destaque = df_filtered.groupby('vendedor_nome')['valor_venda'].sum().idxmax() if len(df_filtered) > 0 else "N/A"
valor_vendedor = df_filtered.groupby('vendedor_nome')['valor_venda'].sum().max() / 1e6 if len(df_filtered) > 0 else 0

regiao_destaque = df_filtered.groupby('regiao_nome')['valor_venda'].sum().idxmax() if len(df_filtered) > 0 else "N/A"
valor_regiao = df_filtered.groupby('regiao_nome')['valor_venda'].sum().max() / 1e6 if len(df_filtered) > 0 else 0

mes_destaque_num = df_filtered.groupby('mes')['valor_venda'].sum().idxmax() if len(df_filtered) > 0 else 1
mes_destaque = meses_nomes[int(mes_destaque_num)-1] if mes_destaque_num else "N/A"
valor_mes = df_filtered.groupby('mes')['valor_venda'].sum().max() / 1e6 if len(df_filtered) > 0 else 0

# Cards estilizados
col1, col2, col3, col4, col5 = st.columns(5)

with col1:
    st.markdown(f"""
        <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                    padding: 25px; border-radius: 15px; 
                    box-shadow: 0 8px 16px rgba(102, 126, 234, 0.4);
                    border: 1px solid rgba(255, 255, 255, 0.1);
                    text-align: center;">
            <p style="color: white; font-size: 2.5rem; margin: 0;">🚗</p>
            <p style="color: white; font-size: 0.9rem; font-weight: 600; margin: 10px 0 5px 0; opacity: 0.9;">MODELO MAIS VENDIDO</p>
            <p style="color: white; font-size: 1.3rem; font-weight: 700; margin: 5px 0;">{modelo_destaque}</p>
            <p style="color: white; font-size: 1rem; font-weight: 500; opacity: 0.8; margin: 5px 0 0 0;">{qtd_modelo} unidades</p>
        </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown(f"""
        <div style="background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
                    padding: 25px; border-radius: 15px; 
                    box-shadow: 0 8px 16px rgba(240, 147, 251, 0.4);
                    border: 1px solid rgba(255, 255, 255, 0.1);
                    text-align: center;">
            <p style="color: white; font-size: 2.5rem; margin: 0;">🏢</p>
            <p style="color: white; font-size: 0.9rem; font-weight: 600; margin: 10px 0 5px 0; opacity: 0.9;">MARCA MAIS VENDIDA</p>
            <p style="color: white; font-size: 1.3rem; font-weight: 700; margin: 5px 0;">{marca_destaque}</p>
            <p style="color: white; font-size: 1rem; font-weight: 500; opacity: 0.8; margin: 5px 0 0 0;">R$ {valor_marca:.1f}M</p>
        </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown(f"""
        <div style="background: linear-gradient(135deg, #fa709a 0%, #fee140 100%);
                    padding: 25px; border-radius: 15px; 
                    box-shadow: 0 8px 16px rgba(250, 112, 154, 0.4);
                    border: 1px solid rgba(255, 255, 255, 0.1);
                    text-align: center;">
            <p style="color: white; font-size: 2.5rem; margin: 0;">👔</p>
            <p style="color: white; font-size: 0.9rem; font-weight: 600; margin: 10px 0 5px 0; opacity: 0.9;">MELHOR VENDEDOR</p>
            <p style="color: white; font-size: 1.3rem; font-weight: 700; margin: 5px 0;">{vendedor_destaque}</p>
            <p style="color: white; font-size: 1rem; font-weight: 500; opacity: 0.8; margin: 5px 0 0 0;">R$ {valor_vendedor:.1f}M</p>
        </div>
    """, unsafe_allow_html=True)

with col4:
    st.markdown(f"""
        <div style="background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);
                    padding: 25px; border-radius: 15px; 
                    box-shadow: 0 8px 16px rgba(79, 172, 254, 0.4);
                    border: 1px solid rgba(255, 255, 255, 0.1);
                    text-align: center;">
            <p style="color: white; font-size: 2.5rem; margin: 0;">🌎</p>
            <p style="color: white; font-size: 0.9rem; font-weight: 600; margin: 10px 0 5px 0; opacity: 0.9;">MELHOR REGIÃO</p>
            <p style="color: white; font-size: 1.3rem; font-weight: 700; margin: 5px 0;">{regiao_destaque}</p>
            <p style="color: white; font-size: 1rem; font-weight: 500; opacity: 0.8; margin: 5px 0 0 0;">R$ {valor_regiao:.1f}M</p>
        </div>
    """, unsafe_allow_html=True)

with col5:
    st.markdown(f"""
        <div style="background: linear-gradient(135deg, #43e97b 0%, #38f9d7 100%);
                    padding: 25px; border-radius: 15px; 
                    box-shadow: 0 8px 16px rgba(67, 233, 123, 0.4);
                    border: 1px solid rgba(255, 255, 255, 0.1);
                    text-align: center;">
            <p style="color: white; font-size: 2.5rem; margin: 0;">📅</p>
            <p style="color: white; font-size: 0.9rem; font-weight: 600; margin: 10px 0 5px 0; opacity: 0.9;">MELHOR MÊS</p>
            <p style="color: white; font-size: 1.3rem; font-weight: 700; margin: 5px 0;">{mes_destaque}</p>
            <p style="color: white; font-size: 1rem; font-weight: 500; opacity: 0.8; margin: 5px 0 0 0;">R$ {valor_mes:.1f}M</p>
        </div>
    """, unsafe_allow_html=True)

st.markdown("---")

# Nova Visualização Criativa: Cores mais vendidas por estado
st.subheader("🎨 Visualização Extra: Cores Mais Vendidas por Estado")

cores_estado = df_filtered.groupby(['regiao_estado', 'veiculo_cor'])['venda_id'].count().reset_index()
cores_estado.columns = ['Estado', 'Cor', 'Quantidade']

# Top 3 cores por estado
top_cores_estado = cores_estado.sort_values(['Estado', 'Quantidade'], ascending=[True, False])
top_cores_estado = top_cores_estado.groupby('Estado').head(3)

fig_cores = px.bar(
    top_cores_estado,
    x='Estado',
    y='Quantidade',
    color='Cor',
    title='Top 3 Cores Mais Vendidas por Estado',
    labels={'Quantidade': 'Veículos Vendidos'},
    barmode='group',
    height=400,
    color_discrete_sequence=px.colors.qualitative.Vivid
)
fig_cores.update_layout(
    plot_bgcolor='rgba(0,0,0,0)',
    paper_bgcolor='rgba(0,0,0,0)',
    font=dict(color='white', size=12),
    title_font=dict(size=16, color='white'),
    xaxis=dict(gridcolor='rgba(255,255,255,0.1)', showgrid=False),
    yaxis=dict(gridcolor='rgba(255,255,255,0.1)', showgrid=True),
    legend=dict(
        bgcolor='rgba(0,0,0,0.3)',
        bordercolor='rgba(255,255,255,0.2)',
        borderwidth=1
    ),
    margin=dict(l=10, r=10, t=40, b=10)
)
st.plotly_chart(fig_cores, width='stretch')

# Tabela detalhada
st.markdown("---")
st.subheader("📊 Dados Detalhados")

tab1, tab2, tab3 = st.tabs(["Vendas", "Vendedores", "Regiões"])

with tab1:
    st.dataframe(
        df_filtered[['data_venda', 'veiculo_modelo', 'veiculo_marca', 
                     'valor_venda', 'vendedor_nome', 'cliente_nome', 'regiao_nome']]
        .sort_values('data_venda', ascending=False)
        .head(100),
        width='stretch'
    )

with tab2:
    vendedores_stats = df_filtered.groupby('vendedor_nome').agg({
        'valor_venda': 'sum',
        'venda_id': 'count'
    }).sort_values('valor_venda', ascending=False)
    vendedores_stats.columns = ['Faturamento Total', 'Vendas']
    vendedores_stats['Ticket Médio'] = vendedores_stats['Faturamento Total'] / vendedores_stats['Vendas']
    st.dataframe(vendedores_stats, width='stretch')

with tab3:
    regioes_stats = df_filtered.groupby(['regiao_nome', 'regiao_estado']).agg({
        'valor_venda': 'sum',
        'venda_id': 'count'
    }).sort_values('valor_venda', ascending=False)
    regioes_stats.columns = ['Faturamento Total', 'Vendas']
    st.dataframe(regioes_stats, width='stretch')

# Footer
st.markdown("---")
st.markdown("""
    <div style='text-align: center; color: #666; padding: 20px;'>
        <p>Dashboard BI - Sistema de Vendas de Veículos | Trabalho de Faculdade</p>
        <p>Desenvolvido com Streamlit + SQLite + Plotly</p>
    </div>
""", unsafe_allow_html=True)
