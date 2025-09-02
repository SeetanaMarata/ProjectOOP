import pytest

from src.ecommerce.models import Category, CategoryIterator, Product


class TestProduct:
    """Тесты для класса Product."""

    def test_product_initialization(self) -> None:
        """Тест корректной инициализации товара."""
        product = Product("Test Product", "Test Description", 100.0, 5)

        assert product.name == "Test Product"
        assert product.description == "Test Description"
        assert product.price == 100.0  # Используем геттер
        assert product.quantity == 5

    def test_product_repr(self) -> None:
        """Тест строкового представления товара."""
        product = Product("Test", "Desc", 50.0, 3)
        repr_str = repr(product)

        assert "Test" in repr_str
        assert "50.0" in repr_str

    def test_price_setter_positive(self) -> None:
        """Тест установки корректной цены."""
        product = Product("Test", "Desc", 50.0, 3)
        product.price = 75.0  # Используем сеттер
        assert product.price == 75.0

    def test_price_setter_negative(self, capsys: pytest.CaptureFixture) -> None:
        """Тест установки отрицательной цены."""
        product = Product("Test", "Desc", 50.0, 3)
        product.price = -10.0
        captured = capsys.readouterr()
        assert "Цена не должна быть нулевая или отрицательная" in captured.out
        assert product.price == 50.0  # Цена не изменилась

    def test_new_product_class_method(self) -> None:
        """Тест класс-метода создания товара."""
        product_data = {
            "name": "New Product",
            "description": "New Description",
            "price": "100.0",
            "quantity": "5",
        }

        product = Product.new_product(product_data)
        assert product.name == "New Product"
        assert product.price == 100.0
        assert product.quantity == 5

    def test_new_product_duplicate(self) -> None:
        """Тест создания товара-дубликата."""
        existing_product = Product("Existing", "Desc", 50.0, 3)
        products_list = [existing_product]

        product_data = {
            "name": "Existing",
            "description": "New Desc",
            "price": "75.0",
            "quantity": "2",
        }

        result = Product.new_product(product_data, products_list)
        assert result == existing_product
        assert existing_product.quantity == 5  # 3 + 2
        assert existing_product.price == 75.0  # Выбрана максимальная цена

    def test_product_addition(self) -> None:
        """Тест сложения товаров."""
        product1 = Product("Товар 1", "Описание 1", 100.0, 10)
        product2 = Product("Товар 2", "Описание 2", 200.0, 2)

        result = product1 + product2
        expected = (100.0 * 10) + (200.0 * 2)  # 1000 + 400 = 1400

        assert result == expected

    def test_product_addition_type_error(self) -> None:
        """Тест ошибки при сложении с неправильным типом."""
        product = Product("Товар", "Описание", 100.0, 5)

        with pytest.raises(
            TypeError, match="Можно складывать только объекты класса Product"
        ):
            product + "не товар"


class TestCategory:
    """Тесты для класса Category."""

    def test_category_initialization(self) -> None:
        """Тест корректной инициализации категории."""
        # Сброс счетчиков для чистого теста
        Category.category_count = 0
        Category.product_count = 0

        product1 = Product("P1", "D1", 10.0, 1)
        product2 = Product("P2", "D2", 20.0, 2)

        category = Category("Test Category", "Test Desc", [product1, product2])

        assert category.name == "Test Category"
        assert category.description == "Test Desc"
        # Проверяем через геттер
        assert "P1" in category.products
        assert "P2" in category.products

    def test_add_product_method(self) -> None:
        """Тест метода добавления товара."""
        Category.category_count = 0
        Category.product_count = 0

        product1 = Product("P1", "D1", 10.0, 1)
        product2 = Product("P2", "D2", 20.0, 2)

        category = Category("Test", "Desc", [product1])
        initial_count = Category.product_count

        category.add_product(product2)

        assert Category.product_count == initial_count + 1
        assert "P2" in category.products

    def test_products_property(self) -> None:
        """Тест геттера products."""
        product = Product("Test Product", "Desc", 100.0, 5)
        category = Category("Test", "Desc", [product])

        products_str = category.products
        assert "Test Product" in products_str
        assert "100.0 руб." in products_str
        assert "Остаток: 5 шт." in products_str

    def test_category_counters(self) -> None:
        """Тест подсчета количества категорий и товаров."""
        # Сброс счетчиков
        Category.category_count = 0
        Category.product_count = 0

        product1 = Product("P1", "D1", 10.0, 1)
        product2 = Product("P2", "D2", 20.0, 2)
        product3 = Product("P3", "D3", 30.0, 3)

        # Создаем категории и используем их в assert
        cat1 = Category("Cat1", "Desc1", [product1, product2])
        cat2 = Category("Cat2", "Desc2", [product3])

        # Используем переменные в проверках
        assert Category.category_count == 2
        assert Category.product_count == 3
        assert cat1.name == "Cat1"
        assert cat2.name == "Cat2"

    def test_category_repr(self) -> None:
        """Тест строкового представления категории."""
        product = Product("P1", "D1", 10.0, 1)
        category = Category("Test", "Desc", [product])

        repr_str = repr(category)
        assert "Test" in repr_str
        assert "1" in repr_str

        # Проверяем, что переменная category используется
        assert category.name == "Test"

    def test_category_str_with_quantities(self) -> None:
        """Тест строкового представления категории с учетом количества товаров."""
        product1 = Product("P1", "D1", 10.0, 3)  # quantity = 3
        product2 = Product("P2", "D2", 20.0, 7)  # quantity = 7

        category = Category("Test", "Desc", [product1, product2])

        assert str(category) == "Test, количество продуктов: 10 шт."

    def test_category_iterator(self) -> None:
        """Тест итерации по товарам категории."""
        product1 = Product("P1", "D1", 10.0, 1)
        product2 = Product("P2", "D2", 20.0, 2)

        category = Category("Test", "Desc", [product1, product2])

        # Тестируем итерацию
        products = list(category)
        assert len(products) == 2
        assert products[0].name == "P1"
        assert products[1].name == "P2"

        # Тестируем цикл for
        names = []
        for product in category:
            names.append(product.name)

        assert names == ["P1", "P2"]


class TestCategoryIterator:
    """Тесты для класса CategoryIterator."""

    def test_iterator_initialization(self) -> None:
        """Тест инициализации итератора."""
        product = Product("Test", "Desc", 100.0, 5)
        category = Category("Test", "Desc", [product])
        iterator = CategoryIterator(category)

        assert iterator.category == category
        assert iterator.index == 0

    def test_iterator_next(self) -> None:
        """Тест получения следующего элемента."""
        product1 = Product("P1", "D1", 10.0, 1)
        product2 = Product("P2", "D2", 20.0, 2)
        category = Category("Test", "Desc", [product1, product2])
        iterator = CategoryIterator(category)

        assert next(iterator) == product1
        assert next(iterator) == product2

        with pytest.raises(StopIteration):
            next(iterator)
