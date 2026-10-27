from pathlib import Path
import sys
import traceback

# Додаємо шлях до каталогу src
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from ecommerce_importer.exceptions import RecordValidationError
from ecommerce_importer.validators import parse_product

# Рядок із некоректним нечисловим ID товару
bad_row = {
    "product_id": "abc_wrong_id",
    "name": "Keyboard",
    "category": "electronics",
    "price": "100.0",
    "quantity": "5",
}

print("=== Запуск Експерименту 3: Exception Chaining ===\n")

try:
    parse_product(
        bad_row,
        line_number=15,
        allowed_categories={"electronics"},
    )
except RecordValidationError as error:
    print(f"1. Перехоплено доменний виняток: {error}")
    print(f"2. Пряма першопричина (__cause__): {repr(error.__cause__)}\n")
    print("3. Повний ланцюжок винятків у Traceback:")
    print("--------------------------------------------------")
    # Друкуємо ланцюжок у консоль без аварійного падіння програми
    traceback.print_exc()
    print("--------------------------------------------------")
    print("\n[УСПІХ] Ланцюжок ValueError -> RecordValidationError успішно зафіксовано!")