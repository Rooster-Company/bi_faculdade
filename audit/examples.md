# 📚 EXEMPLOS E CASOS DE USO - BI VENDAS

Este documento contém exemplos práticos de como usar e testar o dashboard BI.

---

## 🎯 EXEMPLO 1: Filtrando por Ano

### Cenário:
Você quer analisar as vendas do ano de 2024.

### Passos:
1. Abra o dashboard (`streamlit run app.py`)
2. No sidebar à esquerda, localize "📅 Selecione o Ano"
3. Escolha "2024" no dropdown
4. Todas as visualizações serão atualizadas automaticamente

### O que você verá:
- **Veículos Vendidos**: Total de unidades vendidas em 2024
- **Faturamento Total**: Soma de todas as vendas em 2024
- **Top 7 Veículos**: Os 7 modelos que mais venderam em 2024
- **Faturamento por Mês**: Gráfico mostrando o desempenho mensal de 2024
- **Destaques**: Melhor modelo, marca, vendedor, região e mês de 2024

---

## 🔍 EXEMPLO 2: Analisando uma Região Específica

### Cenário:
A gerência quer entender o desempenho da região Sul em 2023.

### Passos:
1. Selecione "2023" no filtro de ano
2. No filtro "🌎 Região", escolha "Sul"
3. Observe as métricas atualizadas

### Insights Obtidos:
- Quantos veículos foram vendidos no Sul em 2023
- Qual o faturamento da região
- Quais modelos são mais populares no Sul
- Qual vendedor teve melhor desempenho nesta região

### Query SQL Equivalente:
```sql
SELECT 
    COUNT(*) as total_vendas,
    SUM(v.Valor) as faturamento_total
FROM Vendas v
JOIN Regioes r ON v.RegiaoID = r.ID
WHERE strftime('%Y', v.Data) = '2023'
  AND r.Nome = 'Sul';
```

---

## 📊 EXEMPLO 3: Identificando o Melhor Vendedor

### Cenário:
RH precisa premiar o vendedor com melhor desempenho em 2024.

### Como Encontrar:
1. Filtre o ano para 2024
2. Role até a seção "⭐ Destaques do Ano"
3. Localize o card "👔 MELHOR VENDEDOR"
4. O nome e faturamento serão exibidos

### Alternativa - Tabela Detalhada:
1. Role até o final da página
2. Clique na aba "Vendedores"
3. Veja o ranking completo com:
   - Faturamento Total
   - Número de Vendas
   - Ticket Médio

### Query SQL Equivalente:
```sql
SELECT 
    vd.Nome as vendedor,
    COUNT(*) as total_vendas,
    SUM(v.Valor) as faturamento_total,
    SUM(v.Valor) / COUNT(*) as ticket_medio
FROM Vendas v
JOIN Vendedores vd ON v.VendedorID = vd.ID
WHERE strftime('%Y', v.Data) = '2024'
GROUP BY vd.Nome
ORDER BY faturamento_total DESC
LIMIT 1;
```

---

## 🚗 EXEMPLO 4: Descobrindo Tendências de Cores

### Cenário:
O departamento de compras quer saber quais cores são mais populares em cada estado.

### Como Analisar:
1. Selecione o ano desejado
2. Role até "🎨 Visualização Extra: Cores Mais Vendidas por Estado"
3. Observe o gráfico de barras agrupadas
4. Cada estado mostra suas 3 cores mais vendidas

### Insights Possíveis:
- "No RS, carros pretos vendem mais"
- "Em SP, há preferência por carros brancos"
- "Estados do Nordeste preferem cores claras"

### Query SQL Equivalente:
```sql
WITH RankedCores AS (
    SELECT 
        r.Estado,
        ve.Cor,
        COUNT(*) as quantidade,
        ROW_NUMBER() OVER (PARTITION BY r.Estado ORDER BY COUNT(*) DESC) as ranking
    FROM Vendas v
    JOIN Veiculos ve ON v.VeiculoID = ve.ID
    JOIN Regioes r ON v.RegiaoID = r.ID
    WHERE strftime('%Y', v.Data) = '2024'
    GROUP BY r.Estado, ve.Cor
)
SELECT Estado, Cor, quantidade
FROM RankedCores
WHERE ranking <= 3
ORDER BY Estado, ranking;
```

---

## 📈 EXEMPLO 5: Comparando com Metas

### Cenário:
A diretoria definiu metas de 1042 unidades vendidas e R$ 109M em faturamento.

### Como Verificar:
1. Os KPIs principais (no topo do dashboard) mostram automaticamente:
   - Valor atual vs. meta
   - Delta (diferença) em unidades ou R$
   - Percentual de atingimento

### Interpretação:
- **Verde**: Meta atingida ou superada
- **Vermelho**: Abaixo da meta

### Exemplo de Resultado:
```
🚙 Veículos Vendidos: 1.150
   ↗️ +108 vs meta (1.042)

💰 Faturamento Total: R$ 115.2M
   ↗️ +R$ 6.2M vs meta
```

---

## 🗓️ EXEMPLO 6: Identificando Sazonalidade

### Cenário:
Entender se há meses com maior ou menor volume de vendas.

### Como Analisar:
1. Observe o gráfico "📅 Faturamento por Mês"
2. Identifique picos (barras mais altas) e vales (barras mais baixas)
3. Na seção "Destaques", veja qual foi o melhor mês

### Perguntas Respondidas:
- Há sazonalidade nas vendas?
- Dezembro é melhor que janeiro?
- Há meses com faturamento zero?

### Query SQL para Sazonalidade:
```sql
SELECT 
    strftime('%m', Data) as mes,
    COUNT(*) as vendas,
    SUM(Valor) as faturamento,
    AVG(Valor) as ticket_medio
FROM Vendas
WHERE strftime('%Y', Data) = '2024'
GROUP BY strftime('%m', Data)
ORDER BY mes;
```

---

## 🏆 EXEMPLO 7: Top 7 Veículos - Análise Detalhada

### Cenário:
Identificar os modelos campeões de venda para negociar melhores condições com fornecedores.

### Informações Disponíveis:
- **Faturamento Total**: Em R$ milhões
- **Quantidade Vendida**: Número de unidades

### Como Usar:
1. Veja o gráfico "🏆 Top 7 Veículos Mais Vendidos"
2. Modelos estão ordenados por faturamento
3. As barras coloridas facilitam comparação visual

### Query SQL Equivalente:
```sql
SELECT 
    ve.Modelo,
    ve.Marca,
    COUNT(*) as quantidade,
    SUM(v.Valor) as faturamento_total,
    SUM(v.Valor) / 1000000 as faturamento_milhoes
FROM Vendas v
JOIN Veiculos ve ON v.VeiculoID = ve.ID
WHERE strftime('%Y', v.Data) = '2024'
GROUP BY ve.Modelo, ve.Marca
ORDER BY faturamento_total DESC
LIMIT 7;
```

---

## 🔬 EXEMPLO 8: Validando Dados com SQL

### Cenário:
Você quer validar se os números do dashboard estão corretos.

### Teste 1: Contar Total de Vendas
```sql
-- Via SQL
SELECT COUNT(*) 
FROM Vendas 
WHERE strftime('%Y', Data) = '2024';

-- Deve bater com o número em "Veículos Vendidos" no dashboard
```

### Teste 2: Calcular Faturamento Total
```sql
-- Via SQL
SELECT SUM(Valor) / 1000000 as faturamento_milhoes
FROM Vendas 
WHERE strftime('%Y', Data) = '2024';

-- Deve bater com "Faturamento Total" no dashboard
```

### Teste 3: Verificar Melhor Modelo
```sql
-- Via SQL
SELECT 
    ve.Modelo,
    COUNT(*) as quantidade
FROM Vendas v
JOIN Veiculos ve ON v.VeiculoID = ve.ID
WHERE strftime('%Y', v.Data) = '2024'
GROUP BY ve.Modelo
ORDER BY quantidade DESC
LIMIT 1;

-- Deve bater com "Modelo Mais Vendido" nos destaques
```

---

## 📋 EXEMPLO 9: Exportando Dados para Excel

### Cenário:
Você precisa exportar os dados filtrados para análise em Excel.

### Método 1: Via Interface
1. Role até "📊 Dados Detalhados"
2. Escolha a aba desejada (Vendas, Vendedores ou Regiões)
3. Use o botão de download (ícone no canto superior direito da tabela)

### Método 2: Via SQL Direto
```bash
# No terminal
sqlite3 vendas.db

# Exportar para CSV
.mode csv
.output vendas_2024.csv
SELECT * FROM Vendas WHERE strftime('%Y', Data) = '2024';
.output stdout
```

---

## 🎨 EXEMPLO 10: Criando Visualizações Personalizadas

### Cenário:
Você quer criar uma nova análise não prevista no dashboard.

### Exemplo: Vendas por Categoria de Veículo
```python
import pandas as pd
import sqlite3

conn = sqlite3.connect('vendas.db')

query = """
SELECT 
    ve.Categoria,
    COUNT(*) as quantidade,
    SUM(v.Valor) as faturamento
FROM Vendas v
JOIN Veiculos ve ON v.VeiculoID = ve.ID
WHERE strftime('%Y', v.Data) = '2024'
GROUP BY ve.Categoria
ORDER BY faturamento DESC
"""

df = pd.read_sql_query(query, conn)
print(df)

# Resultado:
# Categoria    quantidade    faturamento
# SUV          350          45000000.00
# Sedan        280          38000000.00
# Hatch        220          25000000.00
# ...
```

---

## 🧪 EXEMPLO 11: Testando Integridade dos Dados

### Verificar Vendas sem Veículo
```sql
SELECT COUNT(*) 
FROM Vendas 
WHERE VeiculoID IS NULL;

-- Deve retornar 0
```

### Verificar Vendas sem Vendedor
```sql
SELECT COUNT(*) 
FROM Vendas 
WHERE VendedorID IS NULL;

-- Deve retornar 0
```

### Verificar Consistência de Valores
```sql
-- Valores negativos (não deveria ter)
SELECT COUNT(*) 
FROM Vendas 
WHERE Valor < 0;

-- Deve retornar 0
```

---

## 💡 DICAS PRÁTICAS

### 1. Performance
- Para análises de múltiplos anos, considere criar views materializadas
- Índices podem acelerar queries frequentes

### 2. Manutenção
- Faça backup do banco `vendas.db` regularmente
- Execute os testes de auditoria após cada atualização

### 3. Extensibilidade
- Para adicionar novos filtros, modifique a seção de sidebar em `app.py`
- Para novas visualizações, adicione após a linha 480 em `app.py`

### 4. Documentação
- Mantenha o `instruções.md` atualizado
- Documente mudanças no esquema do banco

---

## 📞 TROUBLESHOOTING

### Problema: "Nenhum dado disponível"
**Solução**: Execute `python create_sample_db.py` para gerar dados de exemplo

### Problema: "Erro ao carregar dados"
**Solução**: Verifique se o arquivo `vendas.db` existe no diretório

### Problema: Gráficos não aparecem
**Solução**: Instale dependências: `pip install -r requirements.txt`

### Problema: Filtros não funcionam
**Solução**: Limpe o cache: `streamlit cache clear`

---

**Última Atualização**: 04/11/2025  
**Versão**: 1.0
