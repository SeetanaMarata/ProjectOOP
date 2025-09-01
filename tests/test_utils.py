import json
from pathlib import Path

from src.ecommerce.models import Category
from src.ecommerce.utils import load_products_from_json


class TestUtils:
    """Тесты для утилит."""

    def test_load_products_from_json(self, tmp_path: Path) -> None:
        """Тест загрузки данных из JSON."""
        # Создаем временный JSON-файл
        test_data = [
            {
                "name": "Test Category",
                "description": "Test Description",
                "products": [
                    {
                        "name": "Test Product",
                        "description": "Product Desc",
                        "price": "100.0",
                        "quantity": "5",
                    }
                ],
            }
        ]

        test_file = tmp_path / "test_products.json"
        with open(test_file, "w", encoding="utf-8") as f:
            json.dump(test_data, f, ensure_ascii=False)

        # Сброс счетчиков
        Category.category_count = 0
        Category.product_count = 0

        # Загружаем данные
        categories = load_products_from_json(str(test_file))

        assert len(categories) == 1
        assert categories[0].name == "Test Category"
        assert len(categories[0].products) == 1
        assert categories[0].products[0].name == "Test Product"

    def test_load_nonexistent_file(self) -> None:
        """Тест загрузки из несуществующего файла."""
        categories = load_products_from_json("nonexistent.json")
        assert categories == []
