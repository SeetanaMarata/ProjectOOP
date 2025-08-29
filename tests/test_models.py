from src.ecommerce.models import Category, Product


class TestProduct:
    """Тесты для класса Product."""

    def test_product_initialization(self) -> None:
        """Тест корректной инициализации товара."""
        product = Product("Test Product", "Test Description", 100.0, 5)

        assert product.name == "Test Product"
        assert product.description == "Test Description"
        assert product.price == 100.0
        assert product.quantity == 5

    def test_product_repr(self) -> None:
        """Тест строкового представления товара."""
        product = Product("Test", "Desc", 50.0, 3)
        repr_str = repr(product)

        assert "Test" in repr_str
        assert "50.0" in repr_str


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
        assert len(category.products) == 2
        assert category.products[0].name == "P1"

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
