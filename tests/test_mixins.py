import pytest

from src.ecommerce.mixins import ReprMixin
from src.ecommerce.models import Product


class TestReprMixin:
    """Тесты для миксина ReprMixin."""

    def test_repr_mixin_logging(self, capsys: pytest.CaptureFixture) -> None:
        """Тест логирования создания объектов."""
        # Захватываем вывод
        product = Product("Test Product", "Test Description", 100.0, 5)

        captured = capsys.readouterr()
        assert "Создан объект Product с параметрами:" in captured.out
        assert "name='Test Product'" in captured.out
        assert "price=100.0" in captured.out
        assert "quantity=5" in captured.out

        # Используем переменную product для проверки
        assert product.name == "Test Product"
        assert product.price == 100.0
        assert product.quantity == 5

    def test_repr_mixin_repr_method(self) -> None:
        """Тест метода __repr__ миксина."""
        product = Product("Test Product", "Test Description", 100.0, 5)
        repr_str = repr(product)

        assert "Product(" in repr_str
        assert "name='Test Product'" in repr_str
        assert "price=100.0" in repr_str
        assert "quantity=5" in repr_str
        assert "description='Test Description'" in repr_str

        # Используем переменную product для дополнительных проверок
        assert product.description == "Test Description"

    def test_repr_mixin_with_private_attributes(self) -> None:
        """Тест миксина с приватными атрибутами."""

        class TestClass(ReprMixin):
            def __init__(self, public_attr: str, _private_attr: str) -> None:
                self.public_attr = public_attr
                self._private_attr = _private_attr
                super().__init__()

        test_obj = TestClass("public", "private")
        repr_str = repr(test_obj)

        assert "public_attr='public'" in repr_str
        assert (
            "_private_attr" not in repr_str
        )  # Приватные атрибуты не должны отображаться

        # Используем переменную test_obj для проверок
        assert test_obj.public_attr == "public"
        assert test_obj._private_attr == "private"
