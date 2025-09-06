from typing import Dict, List, Optional

from .abstract_models import BaseContainer, BaseProduct
from .exceptions import ZeroQuantityError
from .mixins import ReprMixin


class Product(ReprMixin, BaseProduct):
    """Базовый класс для представления товара."""

    def __init__(self, name: str, description: str, price: float, quantity: int):
        """
        Инициализация товара.

        Args:
            name: Название товара
            description: Описание товара
            price: Цена товара
            quantity: Количество в наличии

        Raises:
            ZeroQuantityError: Если количество равно нулю
        """
        # Проверка на нулевое количество
        if quantity == 0:
            raise ZeroQuantityError(
                "Товар с нулевым количеством не может быть добавлен"
            )

        # 1. Сначала инициализируем все атрибуты BaseProduct
        self.name = name
        self.description = description
        self._price = price
        self.quantity = quantity

        # 2. Затем вызываем миксин (после установки всех атрибутов)
        ReprMixin.__init__(self)

    def __str__(self) -> str:
        return f"{self.name}, {self._price} руб. Остаток: {self.quantity} шт."

    def __add__(self, other: object) -> float:
        if not isinstance(other, Product):
            raise TypeError("Можно складывать только объекты класса Product")

        if type(self) is not type(other):
            raise TypeError("Нельзя складывать товары разных классов")

        return (self.price * self.quantity) + (other.price * other.quantity)

    @property
    def price(self) -> float:
        return self._price

    @price.setter
    def price(self, new_price: float) -> None:
        if new_price <= 0:
            print("Цена не должна быть нулевая или отрицательная")
            return

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
        name = product_data["name"]
        description = product_data["description"]
        price = float(product_data["price"])
        quantity = int(product_data["quantity"])

        if products_list:
            for existing_product in products_list:
                if existing_product.name.lower() == name.lower():
                    # Объединяем количество и выбираем максимальную цену
                    existing_product.quantity += quantity
                    if price > existing_product.price:
                        existing_product.price = price
                    return existing_product

        return cls(name, description, price, quantity)


class Smartphone(Product):
    """Класс для представления смартфона."""

    def __init__(
        self,
        name: str,
        description: str,
        price: float,
        quantity: int,
        efficiency: str,
        model: str,
        memory: int,
        color: str,
    ):
        """
        Инициализация смартфона.
        """
        # 1. Сначала устанавливаем специфичные атрибуты смартфона
        self.efficiency = efficiency
        self.model = model
        self.memory = memory
        self.color = color

        # 2. Затем вызываем родительский конструктор
        super().__init__(name, description, price, quantity)

    def __repr__(self) -> str:
        return (
            f"Smartphone(name='{self.name}', price={self._price}, quantity={self.quantity}, "
            f"model='{self.model}', memory={self.memory})"
        )

    def __str__(self) -> str:
        return (
            f"{self.name} ({self.model}), {self._price} руб. "
            f"Память: {self.memory}GB, Цвет: {self.color}. Остаток: {self.quantity} шт."
        )


class LawnGrass(Product):
    """Класс для представления газонной травы."""

    def __init__(
        self,
        name: str,
        description: str,
        price: float,
        quantity: int,
        country: str,
        germination_period: int,
        color: str,
    ):
        """
        Инициализация газонной травы.
        """
        # 1. Сначала устанавливаем специфичные атрибуты газонной травы
        self.country = country
        self.germination_period = germination_period
        self.color = color

        # 2. Затем вызываем родительский конструктор
        super().__init__(name, description, price, quantity)

    def __repr__(self) -> str:
        return (
            f"LawnGrass(name='{self.name}', price={self._price}, quantity={self.quantity}, "
            f"country='{self.country}', germination={self.germination_period} дней)"
        )

    def __str__(self) -> str:
        return (
            f"{self.name}, {self._price} руб. "
            f"Страна: {self.country}, Прорастание: {self.germination_period} дней, "
            f"Цвет: {self.color}. Остаток: {self.quantity} шт."
        )


class CategoryIterator:
    """Класс-итератор для перебора товаров категории."""

    def __init__(self, category: "Category") -> None:
        self.category = category
        self.products = category.get_products_list()
        self.index = 0

    def __iter__(self) -> "CategoryIterator":
        return self

    def __next__(self) -> Product:
        if self.index < len(self.products):
            product = self.products[self.index]
            self.index += 1
            return product
        raise StopIteration()


class Category(BaseContainer):
    """Класс для представления категории товаров."""

    category_count = 0
    product_count = 0

    def __init__(self, name: str, description: str, products: List[Product]):
        self.name = name
        self.description = description
        self.__products = products

        Category.category_count += 1
        Category.product_count += len(products)

    def __repr__(self) -> str:
        return f"Category(name='{self.name}', products_count={len(self.__products)})"

    def __str__(self) -> str:
        total_quantity = sum(product.quantity for product in self.__products)
        return f"{self.name}, количество продуктов: {total_quantity} шт."

    def __iter__(self) -> CategoryIterator:
        return CategoryIterator(self)

    def add_product(self, product: object) -> None:
        if not isinstance(product, Product):
            raise TypeError(
                "Можно добавлять только объекты класса Product или его наследников"
            )

        self.__products.append(product)
        Category.product_count += 1

    def get_average_price(self) -> float:
        """
        Подсчитывает средний ценник всех товаров в категории.

        Returns:
            Средняя цена товаров или 0, если товаров нет
        """
        try:
            total_price = sum(product.price for product in self.__products)
            return total_price / len(self.__products)
        except ZeroDivisionError:
            return 0.0

    def add_product_with_check(self, product: object) -> None:
        """
        Добавляет товар в категорию с проверкой на нулевое количество.

        Args:
            product: Объект товара для добавления

        Raises:
            ZeroQuantityError: Если количество товара равно нулю
            TypeError: Если переданный объект не является продуктом
        """
        try:
            if not isinstance(product, Product):
                raise TypeError(
                    "Можно добавлять только объекты класса Product или его наследников"
                )

            if product.quantity == 0:
                raise ZeroQuantityError("Нельзя добавить товар с нулевым количеством")

            self.__products.append(product)
            Category.product_count += 1
            print("Товар успешно добавлен")

        except (ZeroQuantityError, TypeError) as e:
            print(f"Ошибка при добавлении товара: {e}")
            raise
        finally:
            print("Обработка добавления товара завершена")

    @property
    def products(self) -> str:
        products_str = ""
        for product in self.__products:
            products_str += f"{product}\n"
        return products_str.rstrip()

    def get_products_list(self) -> List[Product]:
        return self.__products
