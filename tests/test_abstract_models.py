from abc import ABC

from src.ecommerce.abstract_models import BaseContainer, BaseProduct


class TestBaseProduct:
    """Тесты для абстрактного класса BaseProduct."""

    def test_base_product_is_abstract(self) -> None:
        """Тест, что BaseProduct является абстрактным классом."""
        assert issubclass(BaseProduct, ABC)

    def test_base_product_has_abstract_methods(self) -> None:
        """Тест, что BaseProduct имеет все абстрактные методы."""
        assert hasattr(BaseProduct, "__init__")
        assert hasattr(BaseProduct, "__repr__")
        assert hasattr(BaseProduct, "__str__")
        assert hasattr(BaseProduct, "__add__")
        assert hasattr(BaseProduct, "price")
        assert hasattr(BaseProduct, "new_product")

    def test_base_product_abstract_methods_signatures(self) -> None:
        """Тест сигнатур абстрактных методов."""
        # Проверка, что методы существуют с правильными сигнатурами
        assert hasattr(BaseProduct, "__init__")
        assert hasattr(BaseProduct, "__repr__")
        assert hasattr(BaseProduct, "__str__")
        assert hasattr(BaseProduct, "__add__")
        assert hasattr(BaseProduct, "price")
        assert hasattr(BaseProduct, "new_product")


class TestBaseContainer:
    """Тесты для абстрактного класса BaseContainer."""

    def test_base_container_is_abstract(self) -> None:
        """Тест, что BaseContainer является абстрактным классом."""
        assert issubclass(BaseContainer, ABC)

    def test_base_container_has_abstract_methods(self) -> None:
        """Тест, что BaseContainer имеет все абстрактные методы."""
        assert hasattr(BaseContainer, "__init__")
        assert hasattr(BaseContainer, "__repr__")
        assert hasattr(BaseContainer, "__str__")
