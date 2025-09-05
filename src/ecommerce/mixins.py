class ReprMixin:
    """Миксин для логирования создания объектов."""

    def __init__(self, *args: object, **kwargs: object) -> None:
        """Инициализация с логированием параметров."""
        # Не вызываем super(), чтобы избежать проблем с абстрактными классами
        print(
            f"Создан объект {self.__class__.__name__} с параметрами: {self.__repr__()}"
        )

    def __repr__(self) -> str:
        """Строковое представление объекта."""
        attributes = []
        for attr in self.__dict__:
            if not attr.startswith("_"):
                attributes.append(f"{attr}={getattr(self, attr)!r}")
            elif attr == "_price":
                attributes.append(f"price={getattr(self, '_price')!r}")

        return f"{self.__class__.__name__}({', '.join(attributes)})"
