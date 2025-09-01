from typing import List


class Product:
    """Класс для представления товара."""

    def __init__(self, name: str, description: str, price: float, quantity: int):
        """
        Инициализация товара.

        Args:
            name: Название товара
            description: Описание товара
            price: Цена товара
            quantity: Количество в наличии
        """
        self.name = name
        self.description = description
        self.price = price
        self.quantity = quantity

    def __repr__(self) -> str:
        return (
            f"Product(name='{self.name}', price={self.price}, quantity={self.quantity})"
        )

    def __str__(self) -> str:
        return f"{self.name}, {self.price} руб. Остаток: {self.quantity} шт."


class Category:
    """Класс для представления категории товаров."""

    category_count = 0
    product_count = 0

    def __init__(self, name: str, description: str, products: List[Product]):
        """
        Инициализация категории.

        Args:
            name: Название категории
            description: Описание категории
            products: Список товаров в категории
        """
        self.name = name
        self.description = description
        self.products = products

        # Обновляем атрибуты класса
        Category.category_count += 1
        Category.product_count += len(products)

    def __repr__(self) -> str:
        return f"Category(name='{self.name}', products_count={len(self.products)})"

    def __str__(self) -> str:
        return f"{self.name}, количество товаров: {len(self.products)}"