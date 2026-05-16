#!/usr/bin/env python3
"""
SQL Complexity Classifier
Classifica consultas SQL em: Basic, Advanced, Ultra ou Expert
"""

import csv
import re
import sys
from pathlib import Path

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

# ── Componentes SQL ────────────────────────────────────────────────────────

# Componente 1 – Cláusulas Básicas
COMPONENT_1 = [
    'GROUP BY', 'ORDER BY',
    'BETWEEN', 'HAVING', 'WHERE', 'LIMIT', 'JOIN',
    'LIKE', 'AND', 'ASC', 'DESC', 'OR',
]

# Componente 2 – Agregação e Funções
COMPONENT_2 = [
    'TIMESTAMPDIFF', 'JULIANDAY', 'STRFTIME', 'COALESCE', 'DATETIME',
    'DISTINCT', 'DATEDIFF', 'INTEGER', 'GETDATE', 'DATEADD', 'CONCAT',
    'SUBSTR', 'FLOAT', 'MONTH', 'ROUND', 'COUNT', 'LENGTH',
    'YEAR', 'TIME', 'CAST', 'DATE', 'AVG', 'SUM', 'MIN', 'ABS', 'INT',
]

# Componente 3 – Subconsultas e Operações de Conjunto
COMPONENT_3_KEYWORDS = ['INTERSECT', 'EXCEPT', 'UNION']

# Componente 4 – Expressões Condicionais
COMPONENT_4 = ['CASE', 'WHEN', 'THEN', 'ELSE']

# ── Utilitários ────────────────────────────────────────────────────────────

def clean_sql(sql: str) -> str:
    sql = re.sub(r"'(?:[^'\\]|\\.)*'", " ", sql)
    sql = re.sub(r'"(?:[^"\\]|\\.)*"', " ", sql)
    sql = re.sub(r'--[^\n]*', ' ', sql)
    sql = re.sub(r'/\*.*?\*/', ' ', sql, flags=re.DOTALL)
    return sql.upper()


def count_occurrences(text: str, keyword: str) -> int:
    parts = [re.escape(w) for w in keyword.split()]
    pattern = r'\b' + r'\s+'.join(parts) + r'\b'
    return len(re.findall(pattern, text))


def find_keywords(sql_clean: str, keywords: list) -> dict:
    found = {}
    for kw in keywords:
        n = count_occurrences(sql_clean, kw)
        if n > 0:
            found[kw] = n
    return found


def analyze(sql: str) -> dict:
    cleaned = clean_sql(sql)
    c1 = find_keywords(cleaned, COMPONENT_1)
    c2 = find_keywords(cleaned, COMPONENT_2)
    c3 = find_keywords(cleaned, COMPONENT_3_KEYWORDS)
    c4 = find_keywords(cleaned, COMPONENT_4)

    n_select = count_occurrences(cleaned, 'SELECT')
    if n_select > 1:
        c3['SELECT(multi)'] = n_select - 1

    return {'c1': c1, 'c2': c2, 'c3': c3, 'c4': c4}


# ── Classificação ──────────────────────────────────────────────────────────

def classify(sql: str) -> tuple:
    """Retorna (categoria, componentes, motivo)."""
    comps = analyze(sql)
    c1, c2, c3, c4 = comps['c1'], comps['c2'], comps['c3'], comps['c4']

    c1_all_once = all(v == 1 for v in c1.values())
    n_c1 = len(c1)
    n_c2 = len(c2)
    n_c3 = len(c3)
    n_total = n_c1 + n_c2 + n_c3

    if not c2 and not c3 and not c4 and c1_all_once:
        return (
            'Basic', comps,
            "Contém apenas palavras-chave do Componente 1, "
            "cada uma aparecendo no máximo uma vez.",
        )

    if c4:
        kws = ', '.join(sorted(c4))
        return (
            'Ultra', comps,
            f"Condição ①: contém palavra(s)-chave do Componente 4: {kws}.",
        )

    if n_total > 7:
        return (
            'Ultra', comps,
            f"Condição ②: sem Componente 4, mas total de palavras-chave "
            f"distintas (C1+C2+C3) = {n_total} > 7.",
        )

    if n_c3 <= 3 and not c4 and n_c2 < 2:
        return (
            'Advanced', comps,
            f"Condição ①: {n_c3} tipo(s) de C3 (≤3), sem C4, "
            f"{n_c2} tipo(s) de C2 (<2).",
        )

    if n_c3 == 1 and not c4 and n_c2 < 3 and c1_all_once:
        return (
            'Advanced', comps,
            f"Condição ②: exatamente 1 tipo de C3, sem C4, "
            f"{n_c2} tipo(s) de C2 (<3), cada C1 aparece no máximo uma vez.",
        )

    return (
        'Expert', comps,
        "Não se enquadra em Basic, Advanced ou Ultra.",
    )


# ── Relatório ──────────────────────────────────────────────────────────────

COMP_LABELS = {
    'c1': 'Componente 1 – Cláusulas Básicas',
    'c2': 'Componente 2 – Agregação e Funções',
    'c3': 'Componente 3 – Subconsultas e Operações de Conjunto',
    'c4': 'Componente 4 – Expressões Condicionais',
}


def format_report(sql: str) -> str:
    category, comps, reason = classify(sql)
    lines = [
        "=" * 62,
        f"  CLASSIFICAÇÃO: {category.upper()}",
        "=" * 62,
        f"  Motivo: {reason}",
        "",
        "  Palavras-chave encontradas:",
    ]
    for key, label in COMP_LABELS.items():
        kws = comps[key]
        if kws:
            items = ', '.join(f"{k}({v}x)" for k, v in sorted(kws.items()))
            lines.append(f"    {label}:\n      {items}")
        else:
            lines.append(f"    {label}: (nenhuma)")
    lines.append("=" * 62)
    return '\n'.join(lines)


# ── Processamento em lote ──────────────────────────────────────────────────

def process_folder(folder: Path, output_csv: Path, graf_dir: Path) -> None:
    """Classifica todos os .sql da pasta e grava o resultado em CSV."""
    sql_files = sorted(folder.glob('*.sql'))
    if not sql_files:
        print(f"Nenhum arquivo .sql encontrado em '{folder}'.", file=sys.stderr)
        sys.exit(1)

    rows = []
    for path in sql_files:
        sql = path.read_text(encoding='utf-8')
        category, _, _ = classify(sql)
        rows.append({'arquivo': path.name, 'classificacao': category})
        print(f"  {path.name:<30} → {category}")

    output_csv.parent.mkdir(parents=True, exist_ok=True)
    with output_csv.open('w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=['arquivo', 'classificacao'])
        writer.writeheader()
        writer.writerows(rows)

    print(f"\nCSV gerado: {output_csv}  ({len(rows)} arquivo(s) processado(s))")
    gerar_graficos(rows, graf_dir)


# ── Gráficos ───────────────────────────────────────────────────────────────

CATEGORIAS = ['Basic', 'Advanced', 'Ultra', 'Expert']
CORES = ['#4CAF50', '#2196F3', '#FF9800', '#F44336']


def gerar_graficos(rows: list, graf_dir: Path) -> None:
    """Gera gráfico de pizza e tabela de contagem por complexidade."""
    graf_dir.mkdir(parents=True, exist_ok=True)

    counts = {cat: sum(1 for r in rows if r['classificacao'] == cat) for cat in CATEGORIAS}
    total = sum(counts.values())

    _gerar_pizza(counts, graf_dir)
    _gerar_tabela(counts, total, graf_dir)


def _gerar_pizza(counts: dict, graficos_dir: Path) -> None:
    valores = [counts[c] for c in CATEGORIAS]
    entradas = [(v, f"{c}\n({v})", cor) for v, c, cor in zip(valores, CATEGORIAS, CORES) if v > 0]

    fig, ax = plt.subplots(figsize=(7, 6))
    if entradas:
        vs, ls, cs = zip(*entradas)
        _, _, autotexts = ax.pie(
            vs, labels=ls, colors=cs,
            autopct='%1.1f%%', startangle=140,
            pctdistance=0.75,
        )
        for at in autotexts:
            at.set_fontsize(10)
            at.set_fontweight('bold')

    ax.set_title('Distribuição de Complexidade SQL', fontsize=14, fontweight='bold', pad=16)

    caminho = graficos_dir / 'pizza_complexidade.png'
    fig.savefig(caminho, dpi=150, bbox_inches='tight')
    plt.close(fig)
    print(f"Gráfico de pizza salvo: {caminho}")


def _gerar_tabela(counts: dict, total: int, graficos_dir: Path) -> None:
    linhas = []
    for cat in CATEGORIAS:
        n = counts[cat]
        pct = f"{100 * n / total:.1f}%" if total else "0.0%"
        linhas.append([cat, str(n), pct])
    linhas.append(['TOTAL', str(total), '100%'])

    col_labels = ['Complexidade', 'Quantidade', 'Percentual']

    fig, ax = plt.subplots(figsize=(6, 2.8))
    ax.axis('off')

    tbl = ax.table(
        cellText=linhas,
        colLabels=col_labels,
        loc='center',
        cellLoc='center',
    )
    tbl.auto_set_font_size(False)
    tbl.set_fontsize(12)
    tbl.scale(1.2, 2.0)

    for col in range(len(col_labels)):
        tbl[0, col].set_facecolor('#37474F')
        tbl[0, col].set_text_props(color='white', fontweight='bold')

    for i, cor in enumerate(CORES, start=1):
        for col in range(len(col_labels)):
            tbl[i, col].set_facecolor(cor + '44')

    ultima = len(CATEGORIAS) + 1
    for col in range(len(col_labels)):
        tbl[ultima, col].set_facecolor('#CFD8DC')
        tbl[ultima, col].set_text_props(fontweight='bold')

    ax.set_title('Contagem por Complexidade SQL', fontsize=13, fontweight='bold', pad=14)

    caminho = graficos_dir / 'tabela_complexidade.png'
    fig.savefig(caminho, dpi=150, bbox_inches='tight')
    plt.close(fig)
    print(f"Tabela salva: {caminho}")
