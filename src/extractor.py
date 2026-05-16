#!/usr/bin/env python3
import json
from pathlib import Path


def extract(input_file: Path, output_dir: Path, prefix: str | None = None) -> int:
    """Lê o JSON e salva cada query como arquivo .sql individual.

    O nome do arquivo será sql_{prefix}_{i:04d}.sql quando prefix for informado,
    ou sql_{i:04d}.sql caso contrário.
    """
    output_dir.mkdir(parents=True, exist_ok=True)

    with open(input_file, 'r', encoding='utf-8') as f:
        data = json.load(f)

    count = 0
    for i, entry in enumerate(data, start=1):
        query = entry.get('query', '').strip()
        if query:
            name = f'sql_{prefix}_{i:04d}.sql' if prefix else f'sql_{i:04d}.sql'
            (output_dir / name).write_text(query, encoding='utf-8')
            count += 1

    print(f"{count} arquivo(s) SQL salvos em '{output_dir}/'")
    return count
