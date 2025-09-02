from typing import Dict, List, Optional


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
        self._price = price  # Приватный атрибут цены
        self.quantity = quantity

    def __repr__(self) -> str:
        return f"Product(name='{self.name}', price={self._price}, quantity={self.quantity})"

    def __str__(self) -> str:
        return f"{self.name}, {self._price} руб. Остаток: {self.quantity} шт."

    @property
    def price(self) -> float:
        """Геттер для цены."""
        return self._price

    @price.setter
    def price(self, new_price: float) -> None:
        """Сеттер для цены с проверкой."""
        if new_price <= 0:
            print("Цена не должна быть нулевая или отрицательная")
            return

        # Если цена понижается, запрашиваем подтверждение
        if new_price < self._price:
            confirmation = input(
                f"Цена понижается с {self._price} до {new_price}. Подтвердите действие (y/n): "
            )
            if confirmation.lower() != "y":
                print("Изменение цены отменено")
                return

        self._price = new_price

    @classmethod
    def new_product(
        cls, product_data: Dict, products_list: Optional[List["Product"]] = None
    ) -> "Product":
        """
        Класс-метод для создания нового товара.

        Args:
            product_data: Словарь с данными товара
            products_list: Список существующих товаров для проверки дубликатов

        Returns:
            Созданный объект Product
        """
        name = product_data["name"]
        description = product_data["description"]
        price = float(product_data["price"])
        quantity = int(product_data["quantity"])

        # Проверка на дубликаты
        if products_list:
            for existing_product in products_list:
                if existing_product.name.lower() == name.lower():
                    # Объединяем количество и выбираем максимальную цену
                    existing_product.quantity += quantity
                    if price > existing_product.price:
                        existing_product.price = price
                    return existing_product

        return cls(name, description, price, quantity)


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
        self.__products = products  # Приватный атрибут

        # Обновляем атрибуты класса
        Category.category_count += 1
        Category.product_count += len(products)

    def __repr__(self) -> str:
        return f"Category(name='{self.name}', products_count={len(self.__products)})"

    def __str__(self) -> str:
        return f"{self.name}, количество товаров: {len(self.__products)}"

    def add_product(self, product: Product) -> None:
        """
        Добавляет товар в категорию.

        Args:
            product: Объект товара для добавления
        """
        self.__products.append(product)
        Category.product_count += 1

    @property
    def products(self) -> str:
        """Геттер для списка товаров в виде строки."""
        products_str = ""
        for product in self.__products:
            products_str += f"{product}\n"
        return products_str.rstrip()

    def get_products_list(self) -> List[Product]:
        """Метод для получения списка товаров (для внутреннего использования)."""
        return self.__products
