#!/usr/bin/env python3
import json
from pathlib import Path


def extract(input_file: Path, output_dir: Path) -> int:
    """Lê o JSON e salva cada query como arquivo .sql individual."""
    output_dir.mkdir(parents=True, exist_ok=True)

    with open(input_file, 'r', encoding='utf-8') as f:
        data = json.load(f)

    count = 0
    for i, entry in enumerate(data, start=1):
        query = entry.get('query', '').strip()
        if query:
            (output_dir / f'sql_{i:04d}.sql').write_text(query, encoding='utf-8')
            count += 1

    print(f"{count} arquivo(s) SQL salvos em '{output_dir}/'")
    return count
