from collections.abc import Iterator
import csv
from pathlib import Path

from ecommerce_importer.exceptions import DataImportError


def read_csv_rows(path: Path) -> Iterator[tuple[int, dict[str, str]]]:
    """Потокове читання рядків файлу CSV з генерацією (line_number, row)."""
    try:
        with path.open("r", encoding="utf-8", newline="") as file:
            reader = csv.DictReader(file)
            for line_number, row in enumerate(reader, start=2):
                yield line_number, row
    except OSError as error:
        raise DataImportError(f"Cannot read input file: {path}") from error