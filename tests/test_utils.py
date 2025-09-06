import json
from pathlib import Path

import pytest

from src.ecommerce.models import Category
from src.ecommerce.utils import load_products_from_json


class TestUtils:
    """Тесты для утилит."""

    def test_load_products_from_json(self, tmp_path: Path) -> None:
        """Тест загрузки данных из JSON."""
        # Создаем временный JSON-файл
        test_data: list = [
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
        # Используем внутренний метод для получения списка товаров
        assert len(categories[0].get_products_list()) == 1
        assert categories[0].get_products_list()[0].name == "Test Product"

    def test_load_nonexistent_file(self) -> None:
        """Тест загрузки из несуществующего файла."""
        categories = load_products_from_json("nonexistent.json")
        assert categories == []

    def test_load_products_with_invalid_data(self, tmp_path: Path) -> None:
        """Тест загрузки с некорректными данными."""
        # Создаем JSON с некорректной структурой (не список категорий)
        invalid_data: dict = {"invalid": "data"}

        test_file = tmp_path / "invalid_products.json"
        with open(test_file, "w", encoding="utf-8") as f:
            json.dump(invalid_data, f, ensure_ascii=False)

        # Ожидаем, что функция выбросит исключение при некорректных данных
        with pytest.raises(AttributeError) as exc_info:
            load_products_from_json(str(test_file))
        assert "'str' object has no attribute 'get'" in str(exc_info.value)

    def test_load_products_with_malformed_json(self, tmp_path: Path) -> None:
        """Тест загрузки с битым JSON."""
        test_file = tmp_path / "malformed.json"
        with open(test_file, "w", encoding="utf-8") as f:
            f.write("{invalid json")

        categories = load_products_from_json(str(test_file))
        assert categories == []  # Должен вернуть пустой список при ошибке парсинга

    def test_load_products_empty_list(self, tmp_path: Path) -> None:
        """Тест загрузки с пустым списком категорий."""
        empty_data: list = []  # Добавили аннотацию типа

        test_file = tmp_path / "empty_products.json"
        with open(test_file, "w", encoding="utf-8") as f:
            json.dump(empty_data, f, ensure_ascii=False)

        categories = load_products_from_json(str(test_file))
        assert categories == []  # Должен вернуть пустой список
