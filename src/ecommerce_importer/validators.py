from ecommerce_importer.exceptions import RecordValidationError
from ecommerce_importer.models import Product


def parse_product(
    row: dict[str, str],
    *,
    line_number: int,
    allowed_categories: set[str],
) -> Product:
    """Парсинг та валідація полів сутності Product згідно з бізнес-правилами."""
    # product_id
    try:
        product_id = int(row.get("product_id", "").strip())
        if product_id <= 0:
            raise ValueError("product_id must be a positive integer")
    except (TypeError, ValueError) as error:
        raise RecordValidationError(
            "Invalid product ID",
            line_number=line_number,
            field="product_id",
        ) from error

    # name
    name = row.get("name", "").strip()
    if not name:
        raise RecordValidationError(
            "Product name cannot be empty",
            line_number=line_number,
            field="name",
        )

    # category
    category = row.get("category", "").strip().lower()
    if not category:
        raise RecordValidationError(
            "Category cannot be empty",
            line_number=line_number,
            field="category",
        )
    if category not in allowed_categories:
        raise RecordValidationError(
            f"Category '{category}' is not allowed (permitted: {sorted(allowed_categories)})",
            line_number=line_number,
            field="category",
        )

    # price >= 0
    try:
        price = float(row.get("price", "").strip())
    except (TypeError, ValueError) as error:
        raise RecordValidationError(
            "Invalid price format",
            line_number=line_number,
            field="price",
        ) from error

    if price < 0:
        raise RecordValidationError(
            "Price must be non-negative (>= 0)",
            line_number=line_number,
            field="price",
        )

    # quantity >= 0
    try:
        quantity = int(row.get("quantity", "").strip())
    except (TypeError, ValueError) as error:
        raise RecordValidationError(
            "Invalid quantity format",
            line_number=line_number,
            field="quantity",
        ) from error

    if quantity < 0:
        raise RecordValidationError(
            "Quantity must be non-negative (>= 0)",
            line_number=line_number,
            field="quantity",
        )

    return Product(
        product_id=product_id,
        name=name,
        category=category,
        price=price,
        quantity=quantity,
    )