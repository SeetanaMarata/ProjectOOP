from abc import ABC, abstractmethod
from typing import Dict, List, Optional, Type, TypeVar

# Тип для аннотаций
T = TypeVar("T", bound="BaseProduct")


class BaseProduct(ABC):
    """Абстрактный базовый класс для всех продуктов."""

    @abstractmethod
    def __init__(self, name: str, description: str, price: float, quantity: int):
        """Абстрактный метод инициализации продукта."""
        self.name = name
        self.description = description
        self._price = price
        self.quantity = quantity

    @abstractmethod
    def __repr__(self) -> str:
        """Абстрактный метод строкового представления."""
        pass

    @abstractmethod
    def __str__(self) -> str:
        """Абстрактный метод для пользовательского представления."""
        pass

    @abstractmethod
    def __add__(self, other: object) -> float:
        """Абстрактный метод сложения товаров."""
        pass

    @property
    @abstractmethod
    def price(self) -> float:
        """Абстрактный геттер для цены."""
        pass

    @price.setter
    @abstractmethod
    def price(self, new_price: float) -> None:
        """Абстрактный сеттер для цены."""
        pass

    @classmethod
    @abstractmethod
    def new_product(
        cls: Type[T], product_data: Dict, products_list: Optional[List[T]] = None
    ) -> T:
        """Абстрактный класс-метод для создания нового товара."""
        pass


class BaseContainer(ABC):
    """Абстрактный базовый класс для контейнеров (категорий и заказов)."""

    @abstractmethod
    def __init__(self, name: str, description: str):
        """Абстрактный метод инициализации."""
        self.name = name
        self.description = description

    @abstractmethod
    def __repr__(self) -> str:
        """Абстрактный метод строкового представления."""
        pass

    @abstractmethod
    def __str__(self) -> str:
        """Абстрактный метод для пользовательского представления."""
        pass
