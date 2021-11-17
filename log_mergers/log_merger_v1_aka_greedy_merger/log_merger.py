import argparse
import json

from datetime import datetime as dt
from pathlib import Path
from typing import Dict, List

DT_FORMAT = '%Y-%m-%d %H:%M:%S'


def _parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description='Tool to merge logs.')

    parser.add_argument(
        'input_files',
        type=Path,
        nargs='+',
        help='path to logs',
    )

    parser.add_argument(
        '-o', '--output_file',
        type=Path,
        help='where to put merged log-file',
    )

    return parser.parse_args()


def get_logs(input_files: List[Path]) -> List[Dict[str, str, str]]:
    log = []
    for file in input_files:
        with file.open('rb') as f:
            log.extend(json.loads(line) for line in f)
    return log


def write_file(data: List[Dict[str, str, str]], output_file: Path) -> None:
    with output_file.open('w') as out:
        for entry in data:
            json.dump(entry, out)
            out.write('\n')


def main() -> None:
    args = _parse_args()
    logs = get_logs(args.input_files)
    logs.sort(key=lambda entry: dt.strptime(entry['timestamp'], DT_FORMAT))
    write_file(logs, args.output_file)


if __name__ == '__main__':
    main()
