import json
from typing import List

from .models import Category, Product


def load_products_from_json(file_path: str) -> List[Category]:
    """
    Загружает данные о категориях и товарах из JSON-файла.

    Args:
        file_path: Путь к JSON-файлу

    Returns:
        Список объектов Category
    """
    try:
        with open(file_path, "r", encoding="utf-8") as file:
            data = json.load(file)

        categories = []

        for category_data in data:
            products = []
            for product_data in category_data.get("products", []):
                product = Product(
                    name=product_data["name"],
                    description=product_data["description"],
                    price=float(product_data["price"]),
                    quantity=int(product_data["quantity"]),
                )
                products.append(product)

            category = Category(
                name=category_data["name"],
                description=category_data["description"],
                products=products,
            )
            categories.append(category)

        return categories

    except FileNotFoundError:
        print(f"Файл {file_path} не найден")
        return []
    except json.JSONDecodeError:
        print("Ошибка при чтении JSON-файла")
        return []
    except KeyError as e:
        print(f"Отсутствует обязательное поле в данных: {e}")
        return []
