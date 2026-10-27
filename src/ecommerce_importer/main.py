import logging
from pathlib import Path
import sys

# Додавання шляху до модулів у sys.path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from ecommerce_importer.config import load_config
from ecommerce_importer.exceptions import ApplicationError
from ecommerce_importer.exporters import export_products_json
from ecommerce_importer.logging_config import configure_logging
from ecommerce_importer.services import ImportStatistics, import_products
from ecommerce_importer.utils import logged_operation

logger = logging.getLogger("ecommerce_importer")


def main() -> None:
    try:
        config = load_config(Path("config.yaml"))
        configure_logging(config.logging.level, config.logging.path)
        statistics = ImportStatistics()

        with logged_operation("E-commerce inventory pipeline"):
            products = import_products(
                config.input_path,
                allowed_categories=config.processing.allowed_categories,
                min_stock_threshold=config.processing.min_stock_threshold,
                skip_invalid=config.processing.skip_invalid,
                statistics=statistics,
            )
            exported_count = export_products_json(
                products,
                config.output_path,
            )

        logger.info(
            "Execution completed: Total=%s, valid=%s, invalid=%s, low_stock=%s, exported=%s",
            statistics.total,
            statistics.valid,
            statistics.invalid,
            statistics.low_stock_count,
            exported_count,
        )
    except ApplicationError as error:
        logger.error("Application error: %s", error)
        raise SystemExit(1) from error


if __name__ == "__main__":
    main()