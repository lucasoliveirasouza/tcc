#!/usr/bin/env python3
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent / 'src'))

from extractor import extract          # type: ignore
from classifier import process_folder  # type: ignore

ROOT = Path(__file__).parent

DATASETS = {
    '1': {
        'nome':       'Dataset Jamily Sintético',
        'data_dir':   ROOT / 'data'       / 'dataset_jamily',
        'sqls_dir':   ROOT / 'output'     / 'dataset_jamily'              / 'sqls',
        'graf_dir':   ROOT / 'output'     / 'dataset_jamily'              / 'graficos',
        'resultado':  ROOT / 'resultados' / 'resultado_jamily.csv',
        'prefix_fn':  None,
        'query_key':  'query',
    },
    '2': {
        'nome':       'Dataset Jamily Manual',
        'data_dir':   ROOT / 'data'       / 'dataset_jamily_manual',
        'sqls_dir':   ROOT / 'output'     / 'dataset_jamily_manual'       / 'sqls',
        'graf_dir':   ROOT / 'output'     / 'dataset_jamily_manual'       / 'graficos',
        'resultado':  ROOT / 'resultados' / 'resultado_jamily_manual.csv',
        'prefix_fn':  lambda stem: stem,
        'query_key':  'SQL',
    },
    '3': {
        'nome':       'Dataset Science Benchmark Sintético',
        'data_dir':   ROOT / 'data'       / 'dataset_sciencebenchmark',
        'sqls_dir':   ROOT / 'output'     / 'dataset_sciencebenchmark'    / 'sqls',
        'graf_dir':   ROOT / 'output'     / 'dataset_sciencebenchmark'    / 'graficos',
        'resultado':  ROOT / 'resultados' / 'resultado_sciencebenchmark.csv',
        'prefix_fn':  lambda stem: stem.removeprefix('synth_'),
        'query_key':  'query',
    },
    '4': {
        'nome':       'Dataset Science Benchmark Manual',
        'data_dir':   ROOT / 'data'       / 'dataset_sciencebenchmark_manual',
        'sqls_dir':   ROOT / 'output'     / 'dataset_sciencebenchmark_manual' / 'sqls',
        'graf_dir':   ROOT / 'output'     / 'dataset_sciencebenchmark_manual' / 'graficos',
        'resultado':  ROOT / 'resultados' / 'resultado_sciencebenchmark_manual.csv',
        'prefix_fn':  lambda stem: stem,
        'query_key':  'query',
    },
}

MENU = """
╔══════════════════════════════════════════════════════╗
║        SQL Complexity Analysis Pipeline             ║
╠══════════════════════════════════════════════════════╣
║  1. Dataset Jamily Sintético                         ║
║  2. Dataset Jamily Manual                            ║
║  3. Dataset Science Benchmark Sintético              ║
║  4. Dataset Science Benchmark Manual                 ║
║  0. Sair                                             ║
╚══════════════════════════════════════════════════════╝
"""


def run_dataset(cfg: dict) -> None:
    json_files = sorted(cfg['data_dir'].glob('*.json'))
    if not json_files:
        print(f"Nenhum arquivo JSON encontrado em '{cfg['data_dir']}'.")
        sys.exit(1)

    print(f"\n=== Etapa 1: Extração ({cfg['nome']}) ===")
    for json_file in json_files:
        prefix = cfg['prefix_fn'](json_file.stem) if cfg['prefix_fn'] else None
        extract(json_file, cfg['sqls_dir'], prefix=prefix, query_key=cfg['query_key'])

    print(f"\n=== Etapa 2: Classificação de Complexidade ===")
    cfg['resultado'].parent.mkdir(parents=True, exist_ok=True)
    process_folder(cfg['sqls_dir'], cfg['resultado'], cfg['graf_dir'])


def main():
    print(MENU)
    opcao = input("Escolha uma opção: ").strip()

    if opcao in DATASETS:
        run_dataset(DATASETS[opcao])
    elif opcao == '0':
        print("Saindo.")
        sys.exit(0)
    else:
        print(f"Opção '{opcao}' inválida.")
        sys.exit(1)


if __name__ == '__main__':
    main()
