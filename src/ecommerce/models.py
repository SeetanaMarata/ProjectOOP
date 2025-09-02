from typing import Dict, List, Optional


class Product:
    """Базовый класс для представления товара."""

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

    def __add__(self, other: object) -> float:
        """
        Магический метод сложения для товаров.
        Возвращает сумму произведений цены на количество для двух товаров.

        Args:
            other: Второй объект для сложения

        Returns:
            Сумма стоимости всех товаров двух продуктов

        Raises:
            TypeError: Если other не является объектом класса Product
        """
        if not isinstance(other, Product):
            raise TypeError("Можно складывать только объекты класса Product")

        # Задание 2: Проверка, что товары одного типа
        if type(self) is not type(other):
            raise TypeError("Нельзя складывать товары разных классов")

        return (self.price * self.quantity) + (other.price * other.quantity)

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

        Args:
            name: Название товара
            description: Описание товара
            price: Цена товара
            quantity: Количество в наличии
            efficiency: Производительность
            model: Модель
            memory: Объем встроенной памяти
            color: Цвет
        """
        super().__init__(name, description, price, quantity)
        self.efficiency = efficiency
        self.model = model
        self.memory = memory
        self.color = color

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

        Args:
            name: Название товара
            description: Описание товара
            price: Цена товара
            quantity: Количество в наличии
            country: Страна-производитель
            germination_period: Срок прорастания (дни)
            color: Цвет
        """
        super().__init__(name, description, price, quantity)
        self.country = country
        self.germination_period = germination_period
        self.color = color

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
        """
        Инициализация итератора.

        Args:
            category: Объект категории для итерации
        """
        self.category = category
        self.products = category.get_products_list()
        self.index = 0

    def __iter__(self) -> "CategoryIterator":
        """
        Возвращает сам объект итератора.

        Returns:
            self: Объект итератора
        """
        return self

    def __next__(self) -> Product:
        """
        Возвращает следующий товар в категории.

        Returns:
            Product: Следующий товар в списке

        Raises:
            StopIteration: Когда товары закончились
        """
        if self.index < len(self.products):
            product = self.products[self.index]
            self.index += 1
            return product
        raise StopIteration()


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
        """
        Строкое представление категории.
        Считает общее количество товаров на складе (сумма quantity всех продуктов).
        """
        total_quantity = sum(product.quantity for product in self.__products)
        return f"{self.name}, количество продуктов: {total_quantity} шт."

    def __iter__(self) -> CategoryIterator:
        """
        Возвращает итератор для перебора товаров категории.

        Returns:
            CategoryIterator: Объект итератора для категории
        """
        return CategoryIterator(self)

    def add_product(self, product: object) -> None:
        """
        Добавляет товар в категорию.

        Args:
            product: Объект товара для добавления

        Raises:
            TypeError: Если переданный объект не является продуктом или его наследником
        """
        # Задание 3: Проверка, что добавляемый объект является продуктом или его наследником
        if not isinstance(product, Product):
            raise TypeError(
                "Можно добавлять только объекты класса Product или его наследников"
            )

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
