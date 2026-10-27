from pathlib import Path
import yaml

from ecommerce_importer.exceptions import ConfigurationError
from ecommerce_importer.models import AppConfig, LoggingConfig, ProcessingConfig


def validate_config(config: AppConfig) -> None:
    """Перевірка коректності конфігураційних значень."""
    if config.processing.min_stock_threshold < 0:
        raise ConfigurationError("min_stock_threshold cannot be negative")
    if not config.processing.allowed_categories:
        raise ConfigurationError("allowed_categories list cannot be empty")
    if not config.input_path.exists():
        raise ConfigurationError(f"Input file not found: {config.input_path}")


def load_config(path: Path) -> AppConfig:
    """Безпечне читання та валідація структури YAML конфігурації."""
    try:
        with path.open("r", encoding="utf-8") as file:
            raw = yaml.safe_load(file)
    except FileNotFoundError as error:
        raise ConfigurationError(f"Config file not found: {path}") from error
    except yaml.YAMLError as error:
        raise ConfigurationError(f"YAML parsing error in {path}") from error

    if not isinstance(raw, dict):
        raise ConfigurationError("Root YAML element must be a dictionary")

    try:
        raw_proc = raw["processing"]
        allowed_cats = {str(cat).strip().lower() for cat in raw_proc["allowed_categories"]}

        config = AppConfig(
            input_path=Path(raw["input"]["path"]),
            output_path=Path(raw["output"]["path"]),
            processing=ProcessingConfig(
                min_stock_threshold=int(raw_proc["min_stock_threshold"]),
                allowed_categories=allowed_cats,
                skip_invalid=bool(raw_proc["skip_invalid"]),
            ),
            logging=LoggingConfig(
                level=str(raw["logging"]["level"]),
                path=Path(raw["logging"]["path"]),
            ),
        )
    except (KeyError, TypeError, ValueError) as error:
        raise ConfigurationError("Configuration schema is invalid or has missing keys") from error

    validate_config(config)
    return config