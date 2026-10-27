from pathlib import Path
import sys

# Додаємо шлях до каталогу src
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from ecommerce_importer.exceptions import DataExportError
from ecommerce_importer.exporters import export_products_json
from ecommerce_importer.models import Product

output_path = Path("output/products.json")
tmp_path = output_path.with_suffix(output_path.suffix + ".tmp")

# 1. Записуємо початковий валідний файл
initial_products = [
    Product(101, "Initial Product", "electronics", 50.0, 10)
]
export_products_json(initial_products, output_path)
print(f"1. Створено початковий файл: {output_path.name}")
print(f"   Вміст до аварії: {output_path.read_text(encoding='utf-8').strip()}\n")

# 2. Створюємо генератор, який аварійно падає під час віддачі другого товару
def faulty_generator():
    yield Product(102, "Valid One", "electronics", 99.0, 5)
    raise RuntimeError("Раптовий аварійний збій у генераторі під час експорту!")

print("2. Спроба експорту через генератор з помилкою...")
try:
    export_products_json(faulty_generator(), output_path)
except DataExportError as error:
    print(f"\n3. Перехоплено очікувану помилку: {error}")
    print(f"   Причина винятку: {repr(error.__cause__)}")

# 3. Перевіряємо стан файлової системи
print("\n4. Перевірка цілісності файлової системи:")
print(f"   Чи існує тимчасовий файл '{tmp_path.name}'?: {tmp_path.exists()} (має бути False)")
print(f"   Чи зберігся попередній основний файл '{output_path.name}'?: {output_path.exists()} (має бути True)")
print(f"   Вміст основного файлу після аварії:")
print(output_path.read_text(encoding='utf-8').strip())