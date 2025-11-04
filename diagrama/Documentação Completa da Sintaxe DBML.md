# Documentação Completa da Sintaxe DBML

**Autor:** Manus AI
**Data:** 04 de Novembro de 2025
**Fonte:** [DBML - Full Syntax Docs][1]

## 1. Visão Geral

**DBML (Database Markup Language)** é uma linguagem DSL (Domain-Specific Language) simples e legível, projetada para definir e documentar estruturas de banco de dados.

A sintaxe básica do DBML utiliza:
*   **Chaves `{}`** para envolver definições de blocos (tabelas, índices, enums, etc.).
*   **Colchetes `[]`** para envolver configurações e restrições.
*   **Aspas simples `''`** para valores de *string*.
*   **Aspas duplas `""`** para nomes de colunas com espaços.

**Exemplo Básico:**

```dbml
Table users {
  id integer
  username varchar
  role varchar
  created_at timestamp
}

Table posts {
  id integer [primary key]
  title varchar
  body text [note: 'Conteúdo da postagem']
  user_id integer
  created_at timestamp
}

Ref: posts.user_id > users.id // Relação muitos-para-um
```

## 2. Definição de Projeto (`Project`)

Permite adicionar uma descrição geral e metadados ao projeto.

**Sintaxe:**

```dbml
Project project_name {
  database_type: 'PostgreSQL'
  Note: 'Descrição do projeto'
}
```

## 3. Definição de Esquema (`Schema`)

Um novo esquema é definido implicitamente ao ser referenciado em uma tabela ou enum. Por padrão, se nenhum esquema for especificado, o elemento pertencerá ao esquema `public`.

**Sintaxe:**

```dbml
// Tabela pertencente ao esquema padrão "public"
Table table_name {
  column_name column_type [column_settings]
}

// Tabela pertencente a um esquema específico
Table schema_name.table_name {
  column_name column_type [column_settings]
}
```

## 4. Definição de Tabela (`Table`)

Define a estrutura de uma tabela no banco de dados.

### 4.1. Alias de Tabela

É possível definir um alias para uma tabela, útil para referências mais curtas em relacionamentos.

**Sintaxe:**

```dbml
Table very_long_user_table as U {
  ...
}

Ref: U.id < posts.user_id
```

### 4.2. Notas de Tabela

Adiciona notas de metadados à tabela, visíveis no diagrama.

**Sintaxe:**

```dbml
Table users {
  id integer
  Note: 'Armazena dados do usuário'
}
```

### 4.3. Configurações de Tabela

As configurações são definidas dentro de colchetes `[]` após o nome da tabela.

**Sintaxe:**

```dbml
Table users [headercolor: #3498DB] {
  ...
}
```

| Configuração | Descrição | Exemplo |
| :--- | :--- | :--- |
| `headercolor: <cor>` | Altera a cor do cabeçalho da tabela no diagrama. | `headercolor: #3498DB` |

## 5. Definição de Coluna

Define o nome, tipo de dado e configurações opcionais de uma coluna.

**Sintaxe:**

```dbml
Table buildings {
  address varchar(255) [unique, not null, note: 'Incluir número da unidade']
  id integer [pk, unique, default: 123]
}
```

### 5.1. Tipos de Dados

O DBML suporta todos os tipos de dados, desde que sejam escritos como uma única palavra (removendo espaços).

**Exemplos:** `integer`, `varchar(255)`, `text`, `JSONB`, `decimal(1,2)`.

### 5.2. Configurações de Coluna

As configurações são definidas em colchetes `[]` após o tipo de dado.

| Configuração | Descrição | Exemplo |
| :--- | :--- | :--- |
| `note: 'string'` | Adiciona uma nota de metadados à coluna. | `note: 'ID primário'` |
| `primary key` ou `pk` | Marca a coluna como chave primária. | `pk` |
| `null` | Permite valores nulos (padrão se omitido). | `null` |
| `not null` | Não permite valores nulos. | `not null` |
| `unique` | Garante que todos os valores na coluna sejam únicos. | `unique` |
| `default: valor` | Define um valor padrão para a coluna. | `default: 'direto'` |
| `increment` | Marca a coluna como auto-incremento. | `increment` |
| `` check: `expressão` `` | Adiciona uma expressão de *check* à coluna. | `` check: `value > 0` `` |

### 5.3. Valor Padrão (`Default Value`)

O valor padrão pode ser de diferentes tipos:

| Tipo de Valor | Sintaxe | Exemplo |
| :--- | :--- | :--- |
| **Número** | Valor numérico simples. | `default: 123` |
| **String** | Envolvido em aspas simples. | `default: 'algum valor'` |
| **Expressão** | Envolvido em *backticks* `` ` ``. | `` default: `now()` `` |
| **Booleano/Nulo** | `true`, `false` ou `null`. | `default: false` |

## 6. Definição de Checagem (`Check`)

Permite especificar restrições de checagem personalizadas, inclusive envolvendo múltiplas colunas.

**Sintaxe:**

```dbml
Table users {
  id integer
  wealth integer
  debt integer
  
  checks {
    `debt + wealth >= 0` [name: 'chk_positive_money']
  }
}
```

A configuração `name` é opcional e define o nome da restrição de checagem.

## 7. Definição de Índice (`Index`)

Permite definir índices de coluna única, compostos ou baseados em expressões.

**Sintaxe:**

```dbml
Table bookings {
  id integer
  country varchar
  created_at timestamp
  
  indexes {
    (id, country) [pk] // Chave primária composta
    created_at [name: 'created_at_index', note: 'Data']
    (country, booking_date) [unique]
    booking_date [type: hash]
    (`id*2`) // Índice baseado em expressão
  }
}
```

### 7.1. Configurações de Índice

| Configuração | Descrição | Exemplo |
| :--- | :--- | :--- |
| `type` | Tipo de índice (ex: `btree`, `hash`). | `type: hash` |
| `name` | Nome do índice. | `name: 'idx_nome'` |
| `unique` | Marca o índice como único. | `unique` |
| `pk` | Marca o índice como chave primária. | `pk` |

## 8. Relacionamentos e Chaves Estrangeiras (`Ref`)

Define as restrições de chave estrangeira entre tabelas.

### 8.1. Tipos de Relacionamento

Existem 4 tipos de relacionamento, definidos pelo operador:

| Operador | Tipo de Relacionamento | Exemplo |
| :--- | :--- | :--- |
| `<` | Um-para-Muitos (One-to-Many) | `users.id < posts.user_id` |
| `>` | Muitos-para-Um (Many-to-One) | `posts.user_id > users.id` |
| `-` | Um-para-Um (One-to-One) | `users.id - user_infos.user_id` |
| `<>` | Muitos-para-Muitos (Many-to-Many) | `authors.id <> books.id` |

### 8.2. Sintaxes de Definição

O relacionamento pode ser definido de três maneiras:

| Sintaxe | Descrição | Exemplo |
| :--- | :--- | :--- |
| **Inline** | Definido na coluna da tabela. | `user_id integer [ref: > users.id]` |
| **Short Form** | Definido separadamente, em uma única linha. | `Ref: posts.user_id > users.id` |
| **Long Form** | Definido separadamente, em um bloco. | `Ref name_optional { from: posts.user_id to: users.id }` |

### 8.3. Configurações de Relacionamento

As configurações são definidas em colchetes `[]` após a definição do relacionamento (na forma *Short* ou *Long*).

**Exemplo:**

```dbml
Ref: posts.user_id > users.id [delete: cascade, update: no action]
```

| Configuração | Descrição | Valores Possíveis |
| :--- | :--- | :--- |
| `delete` | Ação em caso de exclusão da linha referenciada. | `cascade`, `no action`, `restrict`, `set null`, `set default` |
| `update` | Ação em caso de atualização da chave referenciada. | `cascade`, `no action`, `restrict`, `set null`, `set default` |
| `name` | Nome da restrição de chave estrangeira. | *string* |

## 9. Definição de Enum (`Enum`)

Define um tipo enumerado que pode ser usado como tipo de coluna.

**Sintaxe:**

```dbml
Enum user_status {
  active
  inactive
  pending
}

Table users {
  id integer [pk]
  status user_status
}
```

## 10. Definição de Notas (`Note`)

As notas podem ser definidas em diferentes níveis (Projeto, Tabela, Coluna, Grupo de Tabela).

**Sintaxe:**

```dbml
// Nota de Projeto
Project project_name {
  Note: 'Descrição do projeto'
}

// Nota de Tabela
Table users {
  Note: 'Armazena dados do usuário'
  ...
}

// Nota de Coluna (Inline)
Table users {
  id integer [note: 'ID primário']
  ...
}
```

## 11. Agrupamento de Tabelas (`TableGroup`)

Permite agrupar tabelas logicamente, o que é útil para organização visual no diagrama.

**Sintaxe:**

```dbml
TableGroup user_related_tables {
  users
  user_profiles
  user_sessions
  
  Note: 'Tabelas relacionadas a usuários'
}
```

## 12. Parcial de Tabela (`TablePartial`)

Permite definir um conjunto de campos, configurações e índices comuns para serem reutilizados em múltiplas tabelas.

**Sintaxe:**

```dbml
TablePartial audit_fields {
  created_at timestamp [default: `now()`]
  updated_at timestamp
}

Table posts {
  id integer [pk]
  ~audit_fields // Injeta os campos parciais
  ...
}
```

## 13. Strings Multi-linha

Strings longas, como notas ou descrições, podem ser definidas usando três aspas simples `'''`.

**Sintaxe:**

```dbml
Table posts {
  id integer [pk]
  body text [note: '''
    Este campo armazena o conteúdo completo
    da postagem, permitindo múltiplas linhas.
  ''']
}
```

## 14. Comentários

O DBML suporta comentários de linha única usando `//`.

**Sintaxe:**

```dbml
// Este é um comentário de linha única
Table users {
  id integer // Comentário inline
  ...
}
```

## Referências

[1]: https://dbml.dbdiagram.io/docs/ "DBML - Full Syntax Docs"
