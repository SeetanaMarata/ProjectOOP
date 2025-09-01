from typing import Any, Generator

import pytest

from src.ecommerce.models import Category, Product


@pytest.fixture
def sample_product() -> Product:
    return Product("Test Product", "Test Description", 100.0, 5)


@pytest.fixture
def sample_category(sample_product: Product) -> Category:
    return Category("Test Category", "Test Description", [sample_product])


@pytest.fixture(autouse=True)
def reset_category_counters() -> Generator[None, Any, None]:
    """Фикстура для сброса счетчиков перед каждым тестом."""
    Category.category_count = 0
    Category.product_count = 0
    yield
