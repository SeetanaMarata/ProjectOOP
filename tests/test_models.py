import pytest

from src.ecommerce.abstract_models import BaseContainer, BaseProduct
from src.ecommerce.mixins import ReprMixin
from src.ecommerce.models import Category, LawnGrass, Product, Smartphone


class TestProductInheritance:
    """Тесты для наследования классов продуктов."""

    def test_product_inheritance(self) -> None:
        """Тест, что Product наследуется от BaseProduct и ReprMixin."""
        product = Product("Test", "Desc", 100.0, 5)

        assert isinstance(product, BaseProduct)
        assert isinstance(product, ReprMixin)
        assert hasattr(product, "price")
        assert hasattr(product, "__add__")

    def test_smartphone_inheritance(self) -> None:
        """Тест, что Smartphone наследуется от Product."""
        smartphone = Smartphone(
            "iPhone 15", "Смартфон Apple", 999.99, 10, "Высокая", "15 Pro", 256, "Black"
        )

        assert isinstance(smartphone, Product)
        assert isinstance(smartphone, BaseProduct)
        assert smartphone.name == "iPhone 15"
        assert smartphone.efficiency == "Высокая"
        assert smartphone.model == "15 Pro"
        assert smartphone.memory == 256
        assert smartphone.color == "Black"

    def test_lawn_grass_inheritance(self) -> None:
        """Тест, что LawnGrass наследуется от Product."""
        lawn_grass = LawnGrass(
            "Газонная трава Premium",
            "Качественная трава",
            49.99,
            100,
            "Германия",
            14,
            "Зеленый",
        )

        assert isinstance(lawn_grass, Product)
        assert isinstance(lawn_grass, BaseProduct)
        assert lawn_grass.name == "Газонная трава Premium"
        assert lawn_grass.country == "Германия"
        assert lawn_grass.germination_period == 14
        assert lawn_grass.color == "Зеленый"

    def test_smartphone_repr(self) -> None:
        """Тест строкового представления смартфона."""
        smartphone = Smartphone(
            "Test Phone", "Desc", 100.0, 5, "Medium", "Model X", 128, "Blue"
        )

        repr_str = repr(smartphone)
        assert "Smartphone" in repr_str
        assert "Model X" in repr_str
        assert "128" in repr_str

    def test_lawn_grass_repr(self) -> None:
        """Тест строкового представления газонной травы."""
        lawn_grass = LawnGrass("Test Grass", "Desc", 50.0, 10, "USA", 21, "Green")

        repr_str = repr(lawn_grass)
        assert "LawnGrass" in repr_str
        assert "USA" in repr_str
        assert "21" in repr_str


class TestProductAdditionRestrictions:
    """Тесты ограничений сложения товаров."""

    def test_same_class_addition(self) -> None:
        """Тест сложения товаров одного класса."""
        smartphone1 = Smartphone("Phone 1", "Desc", 100.0, 2, "High", "M1", 64, "Black")
        smartphone2 = Smartphone(
            "Phone 2", "Desc", 200.0, 3, "High", "M2", 128, "White"
        )

        result = smartphone1 + smartphone2
        expected = (100.0 * 2) + (200.0 * 3)  # 200 + 600 = 800
        assert result == expected

    def test_different_class_addition_error(self) -> None:
        """Тест ошибки при сложении товаров разных классов."""
        smartphone = Smartphone("Phone", "Desc", 100.0, 2, "High", "M1", 64, "Black")
        lawn_grass = LawnGrass("Grass", "Desc", 50.0, 10, "USA", 21, "Green")

        with pytest.raises(TypeError, match="Нельзя складывать товары разных классов"):
            smartphone + lawn_grass

    def test_product_with_smartphone_addition_error(self) -> None:
        """Тест ошибки при сложении базового продукта со смартфоном."""
        product = Product("Product", "Desc", 100.0, 2)
        smartphone = Smartphone("Phone", "Desc", 100.0, 2, "High", "M1", 64, "Black")

        with pytest.raises(TypeError, match="Нельзя складывать товары разных классов"):
            product + smartphone

    def test_smartphone_with_product_addition_error(self) -> None:
        """Тест ошибки при сложении смартфона с базовым продуктом."""
        smartphone = Smartphone("Phone", "Desc", 100.0, 2, "High", "M1", 64, "Black")
        product = Product("Product", "Desc", 100.0, 2)

        with pytest.raises(TypeError, match="Нельзя складывать товары разных классов"):
            smartphone + product


class TestCategoryProductRestrictions:
    """Тесты ограничений добавления продуктов в категорию."""

    def test_add_valid_product(self) -> None:
        """Тест добавления валидного продукта."""
        category = Category("Test", "Desc", [])
        product = Product("Test Product", "Desc", 100.0, 5)

        category.add_product(product)
        assert len(category.get_products_list()) == 1

    def test_add_smartphone(self) -> None:
        """Тест добавления смартфона."""
        category = Category("Test", "Desc", [])
        smartphone = Smartphone("Phone", "Desc", 100.0, 2, "High", "M1", 64, "Black")

        category.add_product(smartphone)
        assert len(category.get_products_list()) == 1

    def test_add_lawn_grass(self) -> None:
        """Тест добавления газонной травы."""
        category = Category("Test", "Desc", [])
        lawn_grass = LawnGrass("Grass", "Desc", 50.0, 10, "USA", 21, "Green")

        category.add_product(lawn_grass)
        assert len(category.get_products_list()) == 1

    def test_add_invalid_object_error(self) -> None:
        """Тест ошибки при добавлении невалидного объекта."""
        category = Category("Test", "Desc", [])

        # Тестируем добавление строки
        with pytest.raises(
            TypeError, match="Можно добавлять только объекты класса Product"
        ):
            category.add_product("not a product")

        # Тестируем добавление числа
        with pytest.raises(
            TypeError, match="Можно добавлять только объекты класса Product"
        ):
            category.add_product(123)

        # Тестируем добавление списка
        with pytest.raises(
            TypeError, match="Можно добавлять только объекты класса Product"
        ):
            category.add_product([])


class TestCategoryInheritance:
    """Тесты наследования категории."""

    def test_category_inheritance(self) -> None:
        """Тест, что Category наследуется от BaseContainer."""
        product = Product("Test", "Desc", 100.0, 5)
        category = Category("Test Category", "Desc", [product])

        assert isinstance(category, BaseContainer)
        assert hasattr(category, "name")
        assert hasattr(category, "description")
        assert hasattr(category, "__repr__")
        assert hasattr(category, "__str__")


class TestProductTypeChecking:
    """Тесты проверки типов продуктов."""

    def test_isinstance_check(self) -> None:
        """Тест проверки isinstance."""
        smartphone = Smartphone("Phone", "Desc", 100.0, 2, "High", "M1", 64, "Black")
        lawn_grass = LawnGrass("Grass", "Desc", 50.0, 10, "USA", 21, "Green")
        product = Product("Product", "Desc", 100.0, 2)

        assert isinstance(smartphone, Product)
        assert isinstance(lawn_grass, Product)
        assert isinstance(product, Product)
        assert isinstance(smartphone, Smartphone)
        assert isinstance(lawn_grass, LawnGrass)

    def test_issubclass_check(self) -> None:
        """Тест проверки issubclass."""
        assert issubclass(Smartphone, Product)
        assert issubclass(LawnGrass, Product)
        assert issubclass(Product, Product)  # Класс является подклассом самого себя
        assert issubclass(Product, BaseProduct)
        assert issubclass(Category, BaseContainer)


class TestProductEdgeCases:
    """Тесты для edge cases продуктов."""

    def test_product_price_setter_increase(self) -> None:
        """Тест увеличения цены товара."""
        product = Product("Test", "Desc", 100.0, 5)
        product.price = 150.0
        assert product.price == 150.0

    def test_product_price_setter_zero(self, capsys: pytest.CaptureFixture) -> None:
        """Тест установки нулевой цены."""
        product = Product("Test", "Desc", 100.0, 5)
        product.price = 0  # Должно вызвать предупреждение
        captured = capsys.readouterr()
        assert "Цена не должна быть нулевая или отрицательная" in captured.out
        assert product.price == 100.0  # Цена не должна измениться
