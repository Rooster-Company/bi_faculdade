### **Parte 1 – Modelagem de Dados (0,5)**

**Tarefa:**

Construir o **Diagrama Entidade-Relacionamento (DER)** com base no banco de dados fornecido.

**Entidades obrigatórias:**

- **Veículo** (modelo, marca, categoria, preço unitário)
- **Venda** (data, valor, veículo vendido, vendedor, cliente, região)
- **Vendedor** (nome, ID, região)
- **Cliente** (nome, ID, tipo: pessoa física/jurídica)
- **Região** (nome, estado)
- **Ano** (extraído da data da venda)

**Requisitos:**

- Definir **chaves primárias e estrangeiras**.
- Representar **cardinalidades** entre as entidades.
- O DER deve ser entregue em formato digital (imagem ou PDF).

---

### **📊 Parte 2 – Construção do Dashboard (1,5)**

**Funcionalidades obrigatórias (1,0):**

1. **Filtro de Ano:**
    - Permitir ao usuário selecionar o ano desejado (ex.: 2017, 2018...).
    - Todas as visualizações devem se atualizar automaticamente com base no ano selecionado.
2. **Indicadores Principais:**
    - **Veículos Vendidos:** Total de unidades vendidas no ano.
    - **Meta de Vendas:** Valor fixo para comparação (ex.: 1042 unidades).
    - **Faturamento Total:** Soma dos valores das vendas no ano.
    - **Meta de Faturamento:** Valor fixo para comparação (ex.: R$ 109M).
3. **Top 7 Veículos Vendidos:**
    - Lista dos 7 modelos com maior faturamento no ano.
    - Mostrar valores em milhões (R$M).
4. **Faturamento por Mês:**
    - Gráfico de colunas com o faturamento mês a mês.
    - Eixo X: meses (Jan a Dez), Eixo Y: valores em R$M.
5. **Destaques do Ano:**
    - **Modelo mais vendido**
    - **Marca mais vendida**
    - **Vendedor com maior faturamento**
    - **Região com maior faturamento**
    - **Mês com maior faturamento**
6. **Nova visualização (0,5):**
    - Criar uma nova visualização à escolha da equipe (por exemplo, cores mais vendidas por vendedor em cada estado)
    - Seja criativo!