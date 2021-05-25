import argparse
import json
import os
import time

from datetime import datetime as dt
from functools import total_ordering
from pathlib import Path
from typing import IO, Dict, TextIO, Any

DT_FORMAT = '%Y-%m-%d %H:%M:%S'


@total_ordering
class LogFromFile:

    def __init__(self, f: TextIO):
        self.f = f
        self.line: str = self.f.readline()
        self.file_not_finished: bool = self.is_file_not_finished()
        self.json_line: Dict[str, str] = json.loads(self.line)
        self.dt_timestamp = dt.strptime(self.json_line['timestamp'], DT_FORMAT)

    def __eq__(self, other: Any) -> bool:
        if not hasattr(other, 'dt_timestamp'):
            return NotImplemented
        return self.dt_timestamp == other.dt_timestamp

    def __lt__(self, other: Any) -> bool:
        if not hasattr(other, 'dt_timestamp'):
            return NotImplemented
        return self.dt_timestamp < other.dt_timestamp

    def get_new_line(self) -> None:
        self.line = self.f.readline()
        self.file_not_finished = self.is_file_not_finished()
        self.json_line = json.loads(self.line)
        self.dt_timestamp = dt.strptime(self.json_line['timestamp'], DT_FORMAT)

    def write_line(self, to_file: IO[str], *, update: bool = True) -> None:
        to_file.write(self.line)
        if update:
            self.get_new_line()

    def is_file_not_finished(self) -> bool:
        return not self.f.tell() == os.fstat(self.f.fileno()).st_size


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


def merge_logs(input_file1: Path,
               input_file2: Path,
               output_file: Path) -> None:
    """Построчно сверяет строки и записывает наиболее ранюю строку в файл.
    Если один из файлов закончился, проверяет какой именно и записывает
    строки из оставшегося файла в выходной файл.
    """
    with input_file1.open('r', encoding='utf-8') as f1, \
            input_file2.open('r', encoding='utf-8') as f2, \
            output_file.open('w', encoding='utf-8') as out:
        lines = [
            LogFromFile(f1),
            LogFromFile(f2)
        ]
        while lines[0].file_not_finished and lines[1].file_not_finished:
            line_to_write = lines[0] if lines[0] < lines[1] else lines[1]
            line_to_write.write_line(out)
        else:
            if lines[0].file_not_finished:
                not_finished_file = lines[0]
                finished_file = lines[1]
            else:
                not_finished_file = lines[1]
                finished_file = lines[0]
            finished_file.write_line(out, update=False)
            not_finished_file.write_line(out, update=False)
            remaining_lines = not_finished_file.f.readlines()
            out.writelines(remaining_lines)


def main() -> None:
    t0 = time.time()
    args = _parse_args()
    merge_logs(*args.input_files, args.output_file)
    print(f"finished in {time.time() - t0:.1f} sec")


if __name__ == '__main__':
    main()
