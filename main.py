"""
Основной модуль приложения для управления товарами и категориями.
"""

from src.ecommerce.models import Category, Product
from src.ecommerce.utils import load_products_from_json


def main() -> None:
    """Основная функция приложения."""
    print("=== E-Commerce Management System ===")

    # Сброс счетчиков для чистого теста
    Category.category_count = 0
    Category.product_count = 0

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

    # Демонстрация добавления товара через метод
    print("\n2. Добавление нового товара в категорию:")
    product4 = Product("iPad Air", "Планшет Apple", 699.99, 8)
    laptops.add_product(product4)
    print(f"Добавлен товар: {product4}")

    # Демонстрация геттера products
    print("\n3. Список товаров в категории 'Ноутбуки':")
    print(laptops.products)

    # Демонстрация работы с ценой
    print("\n4. Изменение цены товара:")
    print(f"Текущая цена iPhone 15: {product1.price}")

    # Попытка установить отрицательную цену
    product1.price = -100
    print(f"Цена после попытки установить отрицательное значение: {product1.price}")

    # Корректное изменение цены
    product1.price = 899.99
    print(f"Новая цена iPhone 15: {product1.price}")

    # Показываем статистику
    print("\n5. Статистика:")
    print(f"Всего категорий: {Category.category_count}")
    print(f"Всего товаров: {Category.product_count}")

    # Загрузка данных из JSON
    print("\n6. Загрузка данных из JSON:")
    categories = load_products_from_json("data/products.json")

    if categories:
        print(f"Загружено категорий: {len(categories)}")
        for category in categories:
            print(f"  - {category.name}: {len(category.get_products_list())} товаров")

        # Обновляем статистику
        print("\n7. Обновленная статистика:")
        print(f"Всего категорий: {Category.category_count}")
        print(f"Всего товаров: {Category.product_count}")
    else:
        print("Не удалось загрузить данные из JSON-файла")

    # Демонстрация сложения товаров
    print("\n8. Демонстрация сложения товаров:")
    total_value = product1 + product2
    print(f"Общая стоимость {product1.name} и {product2.name}: {total_value:.2f} руб.")

    # Демонстрация итерации по товарам
    print("\n9. Демонстрация итерации по товарам категории:")
    print("Товары в категории 'Смартфоны':")
    for product in smartphones:
        print(f"  - {product}")

    # Демонстрация нового строкового представления категории
    print("\n10. Демонстрация нового строкового представления:")
    print(f"Категория: {smartphones}")
    print(f"Категория: {laptops}")

    print("\n=== Программа завершена ===")


if __name__ == "__main__":
    main()
