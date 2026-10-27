import csv
from collections.abc import Iterator
from pathlib import Path
from time import perf_counter
import tracemalloc


def generate_dataset(path: Path, count: int) -> None:
    """Генерація тестового набору даних товарів."""
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(["product_id", "name", "category", "price", "quantity"])
        for i in range(1, count + 1):
            writer.writerow([i, f"Product {i}", "electronics", 19.99, 10])


def eager_import(path: Path) -> list[dict[str, str]]:
    """Жадібне (eager) завантаження всього файлу в пам'ять."""
    with path.open("r", encoding="utf-8", newline="") as file:
        return list(csv.DictReader(file))


def streaming_import(path: Path) -> Iterator[dict[str, str]]:
    """Потокове (streaming) зчитування рядків через генератор."""
    with path.open("r", encoding="utf-8", newline="") as file:
        yield from csv.DictReader(file)


def run_benchmark(count: int) -> None:
    path = Path(f"data/benchmark_{count}.csv")
    print(f"\n--- Тестування для {count:,} записів ---")

    if not path.exists():
        print(f"Генерація {count:,} рядків у {path}...")
        generate_dataset(path, count)

    # 1. Тест Eager
    tracemalloc.start()
    start_time = perf_counter()
    data_eager = eager_import(path)
    _ = len(data_eager)
    eager_time = perf_counter() - start_time
    _, eager_peak = tracemalloc.get_traced_memory()
    tracemalloc.stop()

    # Очищуємо змінну перед наступним тестом
    del data_eager

    # 2. Тест Streaming
    tracemalloc.start()
    start_time = perf_counter()
    # Для генератора обов'язково треба пройтися по всіх рядках
    items_count = sum(1 for _ in streaming_import(path))
    streaming_time = perf_counter() - start_time
    _, streaming_peak = tracemalloc.get_traced_memory()
    tracemalloc.stop()

    eager_mb = eager_peak / (1024 * 1024)
    streaming_mb = streaming_peak / (1024 * 1024)

    print(f"Eager:     Час = {eager_time:.4f} s | Пікова RAM = {eager_mb:.2f} MB")
    print(f"Streaming: Час = {streaming_time:.4f} s | Пікова RAM = {streaming_mb:.2f} MB")

    # Видаляємо тимчасовий великий файл після заміру
    path.unlink(missing_ok=True)


if __name__ == "__main__":
    for records in [10_000, 100_000, 500_000]:
        run_benchmark(records)