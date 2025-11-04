# 🎓 Guia Rápido - Apresentação do Diagrama ER

## ⚡ Para a Aula (5 minutos)

### 1️⃣ Opção Mais Rápida: Visualizador Local

```bash
# Na pasta do projeto
cd diagrama
./visualizar_diagrama.sh
# Escolha opção 1 (navegador)
```

**OU** simplesmente abra `diagrama/index.html` no navegador!

---

### 2️⃣ Opção Profissional: dbdiagram.io

1. Abra: https://dbdiagram.io/d
2. Clique no botão **"Copiar DBML"** no `index.html`
3. Cole no editor do dbdiagram.io
4. **Pronto!** Diagrama visual interativo

💡 **Dica**: Você pode exportar como PNG ou PDF direto do site!

---

## 📋 Roteiro de Apresentação

### Introdução (1 min)
> "Desenvolvemos um sistema de vendas de veículos seguindo o modelo Star Schema, otimizado para análises de Business Intelligence."

### Estrutura do Banco (2 min)

**Tabela Fato Central: VENDAS**
- Registra todas as transações
- 5 chaves estrangeiras ligando às dimensões
- Métricas: faturamento, quantidade, ticket médio

**5 Tabelas Dimensão:**
1. **Veículos** → Catálogo de produtos (modelo, marca, categoria, cor, preço)
2. **Vendedores** → Força de vendas
3. **Clientes** → Base segmentada (PF/PJ)
4. **Regiões** → Organização geográfica
5. **Tempo** → Extraído da data (ano/mês)

### Relacionamentos (1 min)

Mostre no diagrama:
- **1:N** - Uma região → Muitos vendedores
- **N:1** - Muitas vendas → Um veículo
- Todas as FKs garantem integridade referencial

### Análises Possíveis (1 min)

Destaque que o modelo permite:
- ✅ Top 7 veículos por faturamento
- ✅ Faturamento mensal
- ✅ Melhor vendedor/região
- ✅ Marca mais vendida
- ✅ Segmentação de clientes

---

## 🎯 Pontos-Chave para Enfatizar

1. **Star Schema** → Padrão de mercado para BI
2. **Índices criados** → Performance otimizada
3. **Documentação completa** → Notas em cada tabela
4. **Queries prontas** → Exemplos práticos incluídos
5. **Escalável** → Suporta crescimento de dados

---

## 💻 Demonstração ao Vivo

### Se tiver internet na aula:

1. Abra `index.html`
2. Clique em **"Ver SQL"** → Mostra o schema completo
3. Clique em **"Abrir dbdiagram.io"** → Visualização interativa
4. Navegue pelo diagrama, mostrando as tabelas e relacionamentos

### Se NÃO tiver internet:

1. Tire screenshots do diagrama antes
2. Prepare um PDF exportado do dbdiagram.io
3. Use o `index.html` local (funciona offline!)

---

## 📊 Slides Sugeridos

### Slide 1: Título
```
DIAGRAMA ENTIDADE-RELACIONAMENTO
Sistema de Vendas de Veículos
[Screenshot do diagrama completo]
```

### Slide 2: Estrutura
```
MODELO STAR SCHEMA
- 1 Tabela Fato (Vendas)
- 5 Tabelas Dimensão
- 5 Relacionamentos principais
[Diagrama simplificado]
```

### Slide 3: Entidades
```
ENTIDADES IMPLEMENTADAS
✓ Veículo (modelo, marca, categoria, preço)
✓ Venda (data, valor, FK's)
✓ Vendedor (nome, região)
✓ Cliente (nome, tipo PF/PJ)
✓ Região (nome, estado)
✓ Ano (dimensão temporal)
```

### Slide 4: Relacionamentos
```
CARDINALIDADES
• Regiões 1:N Vendedores
• Veículos 1:N Vendas
• Vendedores 1:N Vendas
• Clientes 1:N Vendas
• Regiões 1:N Vendas
[Destaque as chaves PK/FK]
```

### Slide 5: Valor para o Negócio
```
ANÁLISES SUPORTADAS
1. Faturamento por período
2. Performance de vendedores
3. Produtos mais vendidos
4. Segmentação geográfica
5. Perfil de clientes
```

---

## 🎤 Falas Sugeridas

**Abertura:**
> "Para atender os requisitos de BI, desenvolvemos um modelo dimensional completo. Utilizamos a técnica Star Schema, que é o padrão de mercado para data warehouses."

**Ao mostrar o diagrama:**
> "No centro, temos a tabela Vendas como nossa tabela fato. Ela se conecta com 5 dimensões: Veículos, Vendedores, Clientes, Regiões e Tempo. Essa estrutura permite fazer queries analíticas com alta performance."

**Relacionamentos:**
> "Todas as cardinalidades estão bem definidas. Por exemplo, uma região pode ter múltiplos vendedores (1:N), mas cada vendedor pertence a apenas uma região. Isso garante a integridade dos dados."

**Fechamento:**
> "Com esse modelo, conseguimos responder todas as perguntas do dashboard: faturamento total, top 7 veículos, melhor vendedor, e muito mais. Tudo com queries otimizadas e índices criados."

---

## ✅ Checklist Pré-Apresentação

- [ ] Testar abertura do `index.html`
- [ ] Verificar se o DBML carrega corretamente
- [ ] Testar botões (copiar, SQL, etc)
- [ ] Preparar screenshots como backup
- [ ] Exportar PDF do dbdiagram.io
- [ ] Revisar queries de exemplo
- [ ] Praticar demonstração (2-3x)

---

## 🚨 Plano B (Se Algo Der Errado)

1. **HTML não abre**: Use os screenshots preparados
2. **dbdiagram.io fora**: Mostre o PDF exportado
3. **Sem internet**: Use o `index.html` local
4. **Falta tempo**: Foque no Star Schema e relacionamentos

---

## 🎁 Material Extra (Se Perguntarem)

**"Por que Star Schema?"**
> "É o padrão para BI porque otimiza queries analíticas. Diferente de um modelo transacional normalizado, aqui priorizamos performance de leitura."

**"E a normalização?"**
> "As dimensões estão em 3FN, mas toleramos alguma desnormalização na tabela fato para ganhar performance. É um trade-off consciente."

**"Quantos dados suporta?"**
> "Com os índices criados, suporta facilmente milhões de registros. SQLite pode chegar a 281 TB teóricos, mas para produção recomendaríamos PostgreSQL."

**"E se precisar de novas análises?"**
> "É só adicionar novos campos nas dimensões ou criar views. A estrutura é flexível e escalável."

---

## 📸 Screenshots Importantes

Prepare antes:

1. ✅ Diagrama completo no dbdiagram.io
2. ✅ Tabela Vendas com todos os campos
3. ✅ Relacionamentos em destaque
4. ✅ Exemplo de query (Top 7 veículos)
5. ✅ Schema SQL gerado

---

## ⏱️ Tempo Estimado

- **Apresentação**: 5 minutos
- **Perguntas**: 2-3 minutos
- **Demonstração**: 2 minutos

**TOTAL: ~10 minutos**

---

**Boa sorte na apresentação! 🚀**

*Você está preparado(a). O material está completo e profissional.* 💪
