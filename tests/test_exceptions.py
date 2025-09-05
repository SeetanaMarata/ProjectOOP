import pytest
from pytest import CaptureFixture

from src.ecommerce.exceptions import ZeroQuantityError
from src.ecommerce.models import Category, Product


class TestZeroQuantityError:
    """Тесты для исключения ZeroQuantityError."""

    def test_zero_quantity_error_creation(self) -> None:
        """Тест создания исключения ZeroQuantityError."""
        error = ZeroQuantityError("Test message")
        assert str(error) == "Test message"
        assert isinstance(error, ValueError)


class TestProductZeroQuantity:
    """Тесты для обработки нулевого количества в Product."""

    def test_product_with_zero_quantity_raises_error(self) -> None:
        """Тест, что товар с нулевым количеством вызывает исключение."""
        with pytest.raises(
            ZeroQuantityError,
            match="Товар с нулевым количеством не может быть добавлен",
        ):
            Product("Test Product", "Description", 100.0, 0)

    def test_product_with_positive_quantity_creates_successfully(self) -> None:
        """Тест, что товар с положительным количеством создается успешно."""
        product = Product("Test Product", "Description", 100.0, 5)
        assert product.quantity == 5


class TestCategoryAveragePrice:
    """Тесты для метода подсчета средней цены в Category."""

    def test_average_price_with_products(self) -> None:
        """Тест подсчета средней цены с товарами."""
        product1 = Product("Product 1", "Desc", 100.0, 5)
        product2 = Product("Product 2", "Desc", 200.0, 3)
        category = Category("Test Category", "Description", [product1, product2])

        assert category.get_average_price() == 150.0

    def test_average_price_empty_category(self) -> None:
        """Тест подсчета средней цены в пустой категории."""
        category = Category("Test Category", "Description", [])
        assert category.get_average_price() == 0.0

    def test_average_price_single_product(self) -> None:
        """Тест подсчета средней цены с одним товаром."""
        product = Product("Product", "Desc", 100.0, 5)
        category = Category("Test Category", "Description", [product])

        assert category.get_average_price() == 100.0


class TestCategoryAddProductWithCheck:
    """Тесты для метода add_product_with_check."""

    def test_add_product_with_check_success(self, capsys: CaptureFixture) -> None:
        """Тест успешного добавления товара."""
        category = Category("Test", "Desc", [])
        product = Product("Test Product", "Desc", 100.0, 5)

        category.add_product_with_check(product)

        captured = capsys.readouterr()
        assert "Товар успешно добавлен" in captured.out
        assert "Обработка добавления товара завершена" in captured.out
        assert len(category.get_products_list()) == 1

    def test_add_product_with_check_zero_quantity(self, capsys: CaptureFixture) -> None:
        """Тест добавления товара с нулевым количеством."""
        category = Category("Test", "Desc", [])

        # Создаем продукт с нулевым количеством (это вызовет исключение в конструкторе)
        with pytest.raises(
            ZeroQuantityError,
            match="Товар с нулевым количеством не может быть добавлен",
        ):
            Product("Test Product", "Desc", 100.0, 0)

        # Для тестирования add_product_with_check нужно создать продукт с положительным количеством,
        # а затем изменить его количество на 0
        product = Product("Test Product", "Desc", 100.0, 5)
        product.quantity = 0  # Меняем количество после создания

        with pytest.raises(
            ZeroQuantityError, match="Нельзя добавить товар с нулевым количеством"
        ):
            category.add_product_with_check(product)

        captured = capsys.readouterr()
        assert "Ошибка при добавлении товара" in captured.out
        assert "Обработка добавления товара завершена" in captured.out
        assert len(category.get_products_list()) == 0

    def test_add_product_with_check_invalid_object(
        self, capsys: CaptureFixture
    ) -> None:
        """Тест добавления невалидного объекта."""
        category = Category("Test", "Desc", [])

        with pytest.raises(
            TypeError, match="Можно добавлять только объекты класса Product"
        ):
            category.add_product_with_check("invalid object")

        captured = capsys.readouterr()
        assert "Ошибка при добавлении товара" in captured.out
        assert "Обработка добавления товара завершена" in captured.out
