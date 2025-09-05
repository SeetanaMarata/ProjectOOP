from typing import Any, Generator

import pytest

from src.ecommerce.models import Category, LawnGrass, Product, Smartphone
from src.ecommerce.orders import Order


@pytest.fixture
def sample_product() -> Product:
    return Product("Test Product", "Test Description", 100.0, 5)


@pytest.fixture
def sample_smartphone() -> Smartphone:
    return Smartphone(
        "Test Phone", "Test Description", 200.0, 3, "High", "Model X", 128, "Black"
    )


@pytest.fixture
def sample_lawn_grass() -> LawnGrass:
    return LawnGrass("Test Grass", "Test Description", 50.0, 10, "USA", 21, "Green")


@pytest.fixture
def sample_category(sample_product: Product) -> Category:
    return Category("Test Category", "Test Description", [sample_product])


@pytest.fixture
def sample_order(sample_product: Product) -> Order:
    return Order(sample_product, 2)


@pytest.fixture(autouse=True)
def reset_category_counters() -> Generator[None, Any, None]:
    """Фикстура для сброса счетчиков перед каждым тестом."""
    Category.category_count = 0
    Category.product_count = 0
    yield
