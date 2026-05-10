# Regras de Classificação de Complexidade SQL

## Componentes SQL

### Componente 1 – Cláusulas Básicas
```
WHERE, GROUP BY, ORDER BY, LIMIT, JOIN,
OR, AND, LIKE, HAVING, BETWEEN, ASC, DESC
```

### Componente 2 – Agregação e Funções
```
DATE, COUNT, AVG, SUM, MIN, DISTINCT, STRFTIME, DATETIME,
SUBSTR, ABS, FLOAT, YEAR, CAST, ROUND, JULIANDAY, TIME,
MONTH, DATEDIFF, TIMESTAMPDIFF, GETDATE, DATEADD, CONCAT,
COALESCE, INTEGER, INT, LENGTH
```

### Componente 3 – Subconsultas e Operações de Conjunto
```
EXCEPT, UNION, INTERSECT, SELECT(múltiplo)
```
> `SELECT(múltiplo)` indica a presença de subconsultas (SELECTs aninhados). Cada SELECT além do primeiro conta como uma ocorrência do Componente 3.

### Componente 4 – Expressões Condicionais
```
CASE, WHEN, THEN, ELSE
```

---

## Categorias de Classificação

### Basic

A consulta contém **apenas** palavras-chave do **Componente 1**, e cada palavra-chave aparece **no máximo uma vez**.

**Exemplo:**
```sql
SELECT nome FROM alunos WHERE idade > 18 ORDER BY nome
```

---

### Advanced

A consulta satisfaz **uma das seguintes condições**:

**Condição ①**
- Contém **até três** tipos de palavras-chave do Componente 3, **e**
- **Não** contém nenhuma palavra-chave do Componente 4, **e**
- Contém **menos de duas** palavras-chave do Componente 2.

**Condição ②**
- Contém **exatamente uma** palavra-chave do Componente 3, **e**
- **Não** contém nenhuma palavra-chave do Componente 4, **e**
- Contém **menos de três** palavras-chave do Componente 2, **e**
- Cada palavra-chave do Componente 1 aparece **no máximo uma vez**.

**Exemplos:**
```sql
-- Condição ①: 1 tipo de C3 (subquery), sem C4, 0 de C2
SELECT nome FROM alunos WHERE id IN (SELECT id FROM aprovados)

-- Condição ②: exatamente 1 C3 (UNION), sem C4, 1 C2 (COUNT), C1 sem repetição
SELECT COUNT(*) FROM a UNION SELECT COUNT(*) FROM b
```

---

### Ultra

A consulta satisfaz **uma das seguintes condições**:

**Condição ①**
- Contém **pelo menos uma** palavra-chave do **Componente 4** (CASE, WHEN, THEN, ELSE).

**Condição ②**
- **Não** contém nenhuma palavra-chave do Componente 4, **mas**
- O total de tipos distintos de palavras-chave dos **Componentes 1, 2 e 3** é **maior que 7**.

**Exemplos:**
```sql
-- Condição ①: contém CASE/WHEN/THEN/ELSE
SELECT nome, CASE WHEN nota >= 7 THEN 'Aprovado' ELSE 'Reprovado' END FROM alunos

-- Condição ②: sem C4, mas muitos tipos de palavras-chave
SELECT AVG(nota), COUNT(*), SUM(horas), MIN(nota), DISTINCT turma
FROM alunos
WHERE ano = 2024 AND status = 'ativo'
GROUP BY turma
ORDER BY AVG(nota) DESC
HAVING COUNT(*) > 5
```

---

### Expert

Qualquer consulta que **não se enquadre** nas categorias **Basic**, **Advanced** ou **Ultra**.

Isso ocorre, por exemplo, quando a consulta tem complexidade intermediária que não atende precisamente às condições de Advanced (como ter dois tipos de palavras-chave do Componente 2 sem subconsultas), mas também não é simples o suficiente para Basic nem atinge os limiares de Ultra.

---

## Ordem de Verificação

O classificador aplica as regras nesta ordem, retornando a primeira categoria que for satisfeita:

```
1. Basic   → apenas C1, cada um ≤ 1 vez
2. Ultra   → C4 presente  OU  total de tipos (C1+C2+C3) > 7
3. Advanced → condição ① OU condição ②
4. Expert  → nenhuma das anteriores
```

---

## Resumo Visual

| Categoria | C4 presente? | Total tipos C1+C2+C3 | Tipos de C3 | Tipos de C2 | C1 cada um ≤1x |
|-----------|:------------:|:--------------------:|:-----------:|:-----------:|:--------------:|
| Basic     | Não          | qualquer             | 0           | 0           | Sim            |
| Advanced① | Não          | ≤ 7                  | ≤ 3         | < 2         | —              |
| Advanced② | Não          | ≤ 7                  | = 1         | < 3         | Sim            |
| Ultra①    | **Sim**      | —                    | —           | —           | —              |
| Ultra②    | Não          | **> 7**              | —           | —           | —              |
| Expert    | —            | —                    | —           | —           | —              |

---

## Uso do Script

```bash
# Passando a consulta como argumento
python medir_complexidade.py "SELECT COUNT(*) FROM vendas WHERE ano = 2024 GROUP BY mes"

# Passando via stdin
echo "SELECT * FROM clientes WHERE cidade = 'SP'" | python medir_complexidade.py

# Modo interativo
python medir_complexidade.py
```
