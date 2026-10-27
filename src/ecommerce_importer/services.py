from collections.abc import Iterator
from dataclasses import dataclass
import logging
from pathlib import Path

from ecommerce_importer.exceptions import RecordValidationError
from ecommerce_importer.models import Product
from ecommerce_importer.readers import read_csv_rows
from ecommerce_importer.validators import parse_product

logger = logging.getLogger(__name__)


@dataclass
class ImportStatistics:
    total: int = 0
    valid: int = 0
    invalid: int = 0
    low_stock_count: int = 0


def import_products(
    path: Path,
    *,
    allowed_categories: set[str],
    min_stock_threshold: int,
    skip_invalid: bool,
    statistics: ImportStatistics,
) -> Iterator[Product]:
    """Потоковий імпорт та перевірка товарів із відстеженням low-stock та невалідних записів."""
    for line_number, row in read_csv_rows(path):
        statistics.total += 1
        try:
            product = parse_product(
                row,
                line_number=line_number,
                allowed_categories=allowed_categories,
            )
        except RecordValidationError as error:
            statistics.invalid += 1
            logger.warning("Invalid record at line %s: %s", error.line_number, error)
            if skip_invalid:
                continue
            raise  # Strict mode: негайне переривання

        # Перевірка порогу низьких залишків
        if product.quantity <= min_stock_threshold:
            statistics.low_stock_count += 1
            logger.warning(
                "Low stock warning: Product ID=%s ('%s') has only %s items left (threshold=%s)",
                product.product_id,
                product.name,
                product.quantity,
                min_stock_threshold,
            )

        statistics.valid += 1
        yield product