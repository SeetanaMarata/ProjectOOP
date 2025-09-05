from src.ecommerce.abstract_models import BaseContainer
from src.ecommerce.models import Product
from src.ecommerce.orders import Order


class TestOrder:
    """Тесты для класса Order."""

    def test_order_creation(self) -> None:
        """Тест создания заказа."""
        product = Product("Test Product", "Desc", 100.0, 5)
        order = Order(product, 3)

        assert order.product == product
        assert order.quantity == 3
        assert order.total_price == 300.0

    def test_order_inheritance(self) -> None:
        """Тест, что Order наследуется от BaseContainer."""
        product = Product("Test", "Desc", 100.0, 5)
        order = Order(product, 3)

        assert isinstance(order, BaseContainer)

    def test_order_repr(self) -> None:
        """Тест строкового представления заказа."""
        product = Product("Test Product", "Desc", 100.0, 5)
        order = Order(product, 3)

        repr_str = repr(order)
        assert "Order(" in repr_str
        assert "product='Test Product'" in repr_str
        assert "quantity=3" in repr_str
        assert "total_price=300.0" in repr_str

    def test_order_str(self) -> None:
        """Тест пользовательского представления заказа."""
        product = Product("Test Product", "Desc", 100.0, 5)
        order = Order(product, 3)

        str_repr = str(order)
        assert "Заказ: Test Product" in str_repr
        assert "количество: 3" in str_repr
        assert "итого: 300.0 руб." in str_repr

    def test_order_with_different_quantities(self) -> None:
        """Тест заказа с разными количествами."""
        product = Product("Test", "Desc", 50.0, 10)

        order1 = Order(product, 1)
        assert order1.total_price == 50.0

        order2 = Order(product, 5)
        assert order2.total_price == 250.0

        order3 = Order(product, 10)
        assert order3.total_price == 500.0
