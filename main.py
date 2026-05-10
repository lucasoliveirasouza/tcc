#!/usr/bin/env python3
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent / 'src'))

from extractor import extract          # type: ignore
from classifier import process_folder, format_report  # type: ignore

ROOT      = Path(__file__).parent
DATA_FILE = ROOT / 'data'   / 'dev_sintetica.json'
SQLS_DIR  = ROOT / 'output' / 'sqls'
RESULTS   = ROOT / 'output' / 'resultados.csv'

MENU = """
╔══════════════════════════════════════╗
║   SQL Complexity Analysis Pipeline  ║
╠══════════════════════════════════════╣
║  1. Extrair SQLs do JSON             ║
║  2. Medir complexidade dos SQLs      ║
║  3. Executar tudo (extração + análise)║
║  0. Sair                             ║
╚══════════════════════════════════════╝
"""


def main():
    print(MENU)
    opcao = input("Escolha uma opção: ").strip()

    if opcao == '1':
        print("\n=== Extração ===")
        extract(DATA_FILE, SQLS_DIR)

    elif opcao == '2':
        print("\n=== Classificação de Complexidade ===")
        process_folder(SQLS_DIR, RESULTS)

    elif opcao == '3':
        print("\n=== Etapa 1: Extração ===")
        extract(DATA_FILE, SQLS_DIR)
        print("\n=== Etapa 2: Classificação de Complexidade ===")
        process_folder(SQLS_DIR, RESULTS)

    elif opcao == '0':
        print("Saindo.")
        sys.exit(0)

    else:
        print(f"Opção '{opcao}' inválida.")
        sys.exit(1)


if __name__ == '__main__':
    main()
