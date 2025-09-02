import json
from typing import List

from .models import Category, LawnGrass, Product, Smartphone


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
        all_products: List[Product] = []

        for category_data in data:
            products: List[Product] = []
            for product_data in category_data.get("products", []):
                # Определяем тип продукта на основе дополнительных полей
                product: Product
                if "efficiency" in product_data and "model" in product_data:
                    product = create_smartphone(product_data, all_products)
                elif "country" in product_data and "germination_period" in product_data:
                    product = create_lawn_grass(product_data, all_products)
                else:
                    product = Product.new_product(product_data, all_products)

                products.append(product)
                all_products.append(product)

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


def create_smartphone(product_data: dict, all_products: List[Product]) -> Smartphone:
    """Создает объект смартфона с проверкой дубликатов."""
    name = product_data["name"]

    # Проверка на дубликаты
    for existing_product in all_products:
        if (
            isinstance(existing_product, Smartphone)
            and existing_product.name.lower() == name.lower()
        ):
            # Объединяем количество и выбираем максимальную цену
            existing_product.quantity += int(product_data["quantity"])
            if float(product_data["price"]) > existing_product.price:
                existing_product.price = float(product_data["price"])
            return existing_product  # type: ignore

    return Smartphone(
        name=name,
        description=product_data["description"],
        price=float(product_data["price"]),
        quantity=int(product_data["quantity"]),
        efficiency=product_data["efficiency"],
        model=product_data["model"],
        memory=int(product_data["memory"]),
        color=product_data["color"],
    )


def create_lawn_grass(product_data: dict, all_products: List[Product]) -> LawnGrass:
    """Создает объект газонной травы с проверкой дубликатов."""
    name = product_data["name"]

    # Проверка на дубликаты
    for existing_product in all_products:
        if (
            isinstance(existing_product, LawnGrass)
            and existing_product.name.lower() == name.lower()
        ):
            # Объединяем количество и выбираем максимальную цену
            existing_product.quantity += int(product_data["quantity"])
            if float(product_data["price"]) > existing_product.price:
                existing_product.price = float(product_data["price"])
            return existing_product  # type: ignore

    return LawnGrass(
        name=name,
        description=product_data["description"],
        price=float(product_data["price"]),
        quantity=int(product_data["quantity"]),
        country=product_data["country"],
        germination_period=int(product_data["germination_period"]),
        color=product_data["color"],
    )
