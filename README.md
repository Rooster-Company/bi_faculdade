# 🚗 Dashboard BI - Vendas de Veículos

Dashboard interativo de Business Intelligence desenvolvido com **Streamlit** e **SQLite** para análise de vendas de veículos.

## 📋 Requisitos Implementados

### ✅ Parte 1 - Modelagem de Dados (0,5)

O banco de dados segue o modelo entidade-relacionamento com:

**Entidades:**
- **Veículos** (modelo, marca, categoria, cor, preço unitário)
- **Vendas** (data, valor, relacionamentos)
- **Vendedores** (nome, ID, região)
- **Clientes** (nome, ID, tipo: PF/PJ)
- **Regiões** (nome, estado)
- **Ano** (extraído da data da venda)

**Relacionamentos:**
- Vendas → Veículos (N:1)
- Vendas → Vendedores (N:1)
- Vendas → Clientes (N:1)
- Vendas → Regiões (N:1)
- Vendedores → Regiões (N:1)

### ✅ Parte 2 - Dashboard (1,5)

**Funcionalidades Obrigatórias (1,0):**

1. **✅ Filtro de Ano**
   - Seleção dinâmica de ano na sidebar
   - Todas visualizações atualizam automaticamente

2. **✅ Indicadores Principais**
   - Veículos Vendidos com meta (1042 unidades)
   - % da Meta de Vendas
   - Faturamento Total com meta (R$ 109M)
   - % da Meta de Faturamento

3. **✅ Top 7 Veículos Vendidos**
   - Gráfico de barras horizontal
   - Valores em milhões (R$M)
   - Ordenado por faturamento

4. **✅ Faturamento por Mês**
   - Gráfico de colunas mensal
   - Eixo X: Jan a Dez
   - Eixo Y: Valores em R$M

5. **✅ Destaques do Ano**
   - Modelo mais vendido
   - Marca mais vendida
   - Vendedor com maior faturamento
   - Região com maior faturamento
   - Mês com maior faturamento

**Nova Visualização (0,5):**

6. **✅ Cores Mais Vendidas por Estado**
   - Gráfico comparativo das top 3 cores por estado
   - Análise regional de preferência de cores
   - Visualização interativa com Plotly

## 🚀 Como Executar

### Opção 1: Com banco Access existente

Se você já tem o arquivo `db.accdb`:

```bash
# 1. Instalar dependências
pip install -r requirements.txt

# 2. Converter Access para SQLite (somente Windows)
python convert_db.py

# 3. Executar o dashboard
streamlit run app.py
```

### Opção 2: Criar banco de exemplo

Se não tiver o Access ou estiver no Linux:

```bash
# 1. Instalar dependências
pip install -r requirements.txt

# 2. Criar banco SQLite com dados de exemplo
python create_sample_db.py

# 3. Executar o dashboard
streamlit run app.py
```

## 📊 Funcionalidades do Dashboard

### Filtros Disponíveis
- **Ano**: Filtro principal que atualiza todas as visualizações
- **Região**: Filtro adicional para análise regional
- **Marca**: Filtro adicional para análise por fabricante

### Visualizações

1. **Cards de KPI**
   - 4 indicadores principais com comparação de metas
   - Deltas coloridos para performance

2. **Top 7 Veículos**
   - Ranking dos modelos mais rentáveis
   - Valores em milhões para melhor leitura

3. **Faturamento Mensal**
   - Tendência de vendas ao longo do ano
   - Identificação de sazonalidade

4. **Destaques do Ano**
   - 5 cards informativos com os principais destaques
   - Informações consolidadas de performance

5. **Análise de Cores por Estado** (EXTRA)
   - Gráfico interativo de preferências regionais
   - Top 3 cores mais vendidas por estado

6. **Tabelas Detalhadas**
   - Aba Vendas: Últimas 100 transações
   - Aba Vendedores: Estatísticas de performance
   - Aba Regiões: Análise regional consolidada

## 🛠️ Tecnologias Utilizadas

- **Streamlit**: Framework para dashboards interativos
- **SQLite**: Banco de dados relacional
- **Pandas**: Manipulação e análise de dados
- **Plotly**: Visualizações interativas
- **Python 3.8+**: Linguagem de programação

## 📁 Estrutura do Projeto

```
bi_faculdade/
├── app.py                  # Dashboard principal
├── create_sample_db.py     # Criação de banco de exemplo
├── convert_db.py           # Conversão Access → SQLite
├── requirements.txt        # Dependências Python
├── README.md              # Este arquivo
├── instruções.md          # Requisitos do trabalho
├── db.accdb               # Banco Access original
└── vendas.db              # Banco SQLite (gerado)
```

## 🎨 Recursos Visuais

- Design responsivo e moderno
- Gráficos interativos com Plotly
- Cards com métricas destacadas
- Cores temáticas e profissionais
- Layout em colunas para melhor aproveitamento

## 📝 Observações

- O banco de exemplo gera dados aleatórios de 2020 a 2024
- Metas são valores fixos para comparação (personalizáveis)
- Todos os gráficos são interativos (zoom, hover, download)
- Dashboard otimizado com cache de dados

## 👥 Trabalho de Faculdade

Desenvolvido como projeto de Business Intelligence para análise de vendas de veículos, contemplando modelagem de dados e construção de dashboard analítico.

---

**Status**: ✅ Completo - Todas as funcionalidades implementadas

**Nota**: Para melhor experiência, use navegador moderno (Chrome, Firefox, Edge)
