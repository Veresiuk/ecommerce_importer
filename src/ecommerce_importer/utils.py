from collections.abc import Iterator
from contextlib import contextmanager
import logging
from time import perf_counter

logger = logging.getLogger(__name__)


@contextmanager
def logged_operation(operation: str) -> Iterator[None]:
    """Контекстний менеджер для таймінгу та діагностики виконання операції."""
    logger.info("%s started", operation)
    start = perf_counter()
    try:
        yield
    except Exception:
        logger.exception("%s failed due to an error", operation)
        raise
    else:
        elapsed = perf_counter() - start
        logger.info("%s finished successfully in %.6f s", operation, elapsed)