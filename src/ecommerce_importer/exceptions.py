class ApplicationError(Exception):
    """Базовий виняток застосунку."""


class ConfigurationError(ApplicationError):
    """Помилка у файлі конфігурації або її валідації."""


class DataError(ApplicationError):
    """Базовий виняток обробки даних."""


class DataImportError(DataError):
    """Помилка відкриття або читання вхідного джерела."""


class DataExportError(DataError):
    """Помилка запису даних під час експорту."""


class RecordValidationError(DataError):
    """Помилка валідації окремого запису товару."""

    def __init__(
        self,
        message: str,
        *,
        line_number: int | None = None,
        field: str | None = None,
    ) -> None:
        super().__init__(message)
        self.line_number = line_number
        self.field = field

    def __str__(self) -> str:
        details = []
        if self.line_number is not None:
            details.append(f"line={self.line_number}")
        if self.field is not None:
            details.append(f"field='{self.field}'")
        if details:
            return f"{super().__str__()} ({', '.join(details)})"
        return super().__str__()