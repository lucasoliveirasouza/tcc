# SQL Complexity Classifier

Ferramenta desenvolvida como parte do Trabalho de Conclusão de Curso (TCC) para classificar automaticamente consultas SQL em quatro níveis de complexidade: **Basic**, **Advanced**, **Ultra** e **Expert**.

---

## Como funciona

A classificação é baseada na detecção de palavras-chave agrupadas em quatro componentes:

| Componente | Descrição | Exemplos |
|---|---|---|
| C1 | Cláusulas Básicas | `WHERE`, `JOIN`, `GROUP BY`, `ORDER BY`, `HAVING`, `LIKE`, `BETWEEN` |
| C2 | Agregação e Funções | `COUNT`, `SUM`, `AVG`, `CAST`, `ROUND`, `DISTINCT`, `DATE`, `COALESCE` |
| C3 | Subconsultas e Conjuntos | `UNION`, `INTERSECT`, `EXCEPT`, múltiplos `SELECT` |
| C4 | Expressões Condicionais | `CASE`, `WHEN`, `THEN`, `ELSE` |

### Regras de classificação

| Nível | Critério |
|---|---|
| **Basic** | Apenas palavras-chave de C1, cada uma aparecendo no máximo uma vez. Sem C2, C3 ou C4. |
| **Advanced** | Presença de C3 (≤ 3 tipos) sem C4, com C2 reduzido (< 2 tipos); ou exatamente 1 tipo de C3, sem C4, com < 3 tipos de C2. |
| **Ultra** | Presença de qualquer palavra-chave de C4; ou total de palavras-chave distintas (C1+C2+C3) > 7. |
| **Expert** | Não se enquadra em nenhuma das categorias acima. |

---

## Datasets utilizados

### 1. Jamily Sintético
Dataset gerado sinteticamente com consultas SQL para o domínio IFG (Instituto Federal de Goiás).

| Arquivo | Perguntas |
|---|---|
| `dev_sintetica.json` | 420 |
| **Total** | **420** |

| Basic | Advanced | Ultra | Expert |
|---|---|---|---|
| 4 (1%) | 158 (37%) | 76 (18%) | 182 (43%) |

---

### 2. Jamily Manual
Conjunto de consultas anotadas manualmente para o mesmo domínio.

| Arquivo | Perguntas |
|---|---|
| `dev.json` | 100 |
| **Total** | **100** |

| Basic | Advanced | Ultra | Expert |
|---|---|---|---|
| 5 (5%) | 4 (4%) | 42 (42%) | 49 (49%) |

---

### 3. Science Benchmark Sintético
Dataset sintético com consultas para três bases científicas: CORDIS, OncoMX e SDSS.

| Arquivo | Perguntas |
|---|---|
| `synth_cordis.json` | 1.306 |
| `synth_oncomx.json` | 1.065 |
| `synth_sdss.json` | 2.061 |
| **Total** | **4.432** |

| Basic | Advanced | Ultra | Expert |
|---|---|---|---|
| 2.848 (64%) | 1.584 (35%) | 0 (0%) | 0 (0%) |

---

### 4. Science Benchmark Manual
Versão manual do Science Benchmark, dividida em conjuntos de desenvolvimento (`dev`) e semente (`seed`).

| Arquivo | Perguntas |
|---|---|
| `dev_cordis.json` | 100 |
| `dev_oncomx.json` | 99 |
| `dev_sdss.json` | 100 |
| `seed_cordis.json` | 100 |
| `seed_oncomx.json` | 100 |
| `seed_sdss.json` | 100 |
| **Total** | **599** |

| Basic | Advanced | Ultra | Expert |
|---|---|---|---|
| 239 (39%) | 330 (55%) | 1 (0%) | 29 (4%) |

---

### 5. Spider 2
Consultas SQL do benchmark Spider 2, fornecidas já extraídas (sem JSON de origem).

| Fonte | Perguntas |
|---|---|
| Arquivos `.sql` pré-extraídos | 256 |
| **Total** | **256** |

| Basic | Advanced | Ultra | Expert |
|---|---|---|---|
| 0 (0%) | 36 (14%) | 198 (77%) | 22 (9%) |

---

## Resumo geral

| Dataset | Total | Basic | Advanced | Ultra | Expert |
|---|---|---|---|---|---|
| Jamily Sintético | 420 | 4 | 158 | 76 | 182 |
| Jamily Manual | 100 | 5 | 4 | 42 | 49 |
| Science Benchmark Sintético | 4.432 | 2.848 | 1.584 | 0 | 0 |
| Science Benchmark Manual | 599 | 239 | 330 | 1 | 29 |
| Spider 2 | 256 | 0 | 36 | 198 | 22 |
| **Total** | **5.807** | **3.096** | **2.112** | **317** | **282** |

---

## Como executar

```bash
python main.py
```

Selecione o dataset no menu interativo. O pipeline executa automaticamente:
1. **Extração** — lê os arquivos JSON e salva cada SQL individualmente em `output/<dataset>/sqls/`
2. **Classificação** — analisa cada SQL e gera o resultado em `resultados/<resultado>.csv`
3. **Gráficos** — gera gráfico de pizza e tabela de distribuição em `output/<dataset>/graficos/`

> O Dataset Spider 2 pula a etapa de extração, pois os arquivos `.sql` já estão pré-extraídos.

---

## Estrutura do projeto

```
.
├── data/
│   ├── dataset_jamily/
│   ├── dataset_jamily_manual/
│   ├── dataset_sciencebenchmark/
│   └── dataset_sciencebenchmark_manual/
├── output/
│   ├── dataset_jamily/
│   ├── dataset_jamily_manual/
│   ├── dataset_sciencebenchmark/
│   ├── dataset_sciencebenchmark_manual/
│   └── dataset_spider2/
├── resultados/
├── src/
│   ├── classifier.py
│   └── extractor.py
├── docs/
│   └── REGRAS_CLASSIFICACAO.md
├── main.py
└── requirements.txt
```
