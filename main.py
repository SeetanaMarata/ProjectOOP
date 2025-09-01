"""
Основной модуль приложения для управления товарами и категориями.
"""

from src.ecommerce.models import Category, Product
from src.ecommerce.utils import load_products_from_json


def main() -> None:
    """Основная функция приложения."""
    print("=== E-Commerce Management System ===")

    # Создаем тестовые данные
    print("\n1. Создание тестовых товаров и категорий:")

    # Создаем товары
    product1 = Product("iPhone 15", "Смартфон Apple", 999.99, 10)
    product2 = Product("Samsung Galaxy", "Смартфон Samsung", 799.99, 15)
    product3 = Product("MacBook Pro", "Ноутбук Apple", 2499.99, 5)

    print(f"Создан товар: {product1}")
    print(f"Создан товар: {product2}")
    print(f"Создан товар: {product3}")

    # Создаем категории
    smartphones = Category("Смартфоны", "Мобильные телефоны", [product1, product2])
    laptops = Category("Ноутбуки", "Портативные компьютеры", [product3])

    print(f"\nСоздана категория: {smartphones}")
    print(f"Создана категория: {laptops}")

    # Показываем статистику
    print("\n2. Статистика:")
    print(f"Всего категорий: {Category.category_count}")
    print(f"Всего товаров: {Category.product_count}")

    # Загрузка данных из JSON
    print("\n3. Загрузка данных из JSON:")
    categories = load_products_from_json("data/products.json")

    if categories:
        print(f"Загружено категорий: {len(categories)}")
        for category in categories:
            print(f"  - {category.name}: {len(category.products)} товаров")

        # Обновляем статистику
        print("\n4. Обновленная статистика:")
        print(f"Всего категорий: {Category.category_count}")
        print(f"Всего товаров: {Category.product_count}")
    else:
        print("Не удалось загрузить данные из JSON-файла")

    print("\n=== Программа завершена ===")


if __name__ == "__main__":
    main()
