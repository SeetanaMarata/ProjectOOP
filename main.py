"""
Основной модуль приложения для управления товарами и категориями.
"""

from src.ecommerce.exceptions import ZeroQuantityError
from src.ecommerce.models import Category, Product
from src.ecommerce.orders import Order


def main() -> None:
    """Основная функция приложения."""
    print("=== E-Commerce Management System ===")

    # Сброс счетчиков для чистого теста
    Category.category_count = 0
    Category.product_count = 0

    # Демонстрация новой функциональности
    print("\n=== Демонстрация новой функциональности ===")

    # 1. Тестирование исключения для нулевого количества
    print("\n1. Тестирование исключения для нулевого количества:")
    try:
        Product("Невалидный товар", "Описание", 100.0, 0)
        print("Ошибка: исключение не было вызвано")
    except ZeroQuantityError as e:
        print(f"✓ Правильно вызвано исключение: {e}")

    # 2. Тестирование среднего ценника
    print("\n2. Тестирование среднего ценника:")
    empty_category = Category("Пустая категория", "Нет товаров", [])
    print(f"Средняя цена в пустой категории: {empty_category.get_average_price()}")

    # Создаем товары для тестирования
    try:
        product1 = Product("Товар 1", "Описание", 100.0, 5)
        product2 = Product("Товар 2", "Описание", 200.0, 3)
        category = Category("Тестовая категория", "Описание", [product1, product2])
        print(f"Средняя цена в категории: {category.get_average_price()}")
    except ZeroQuantityError as e:
        print(f"Ошибка: {e}")

    # 3. Тестирование добавления с проверкой
    print("\n3. Тестирование добавления с проверкой:")
    test_category = Category("Тест", "Описание", [])
    try:
        test_product = Product("Тестовый товар", "Описание", 50.0, 2)
        test_category.add_product_with_check(test_product)
        print(f"Товаров в категории: {len(test_category.get_products_list())}")
    except (ZeroQuantityError, TypeError) as e:
        print(f"Ошибка при добавлении: {e}")

    # 4. Тестирование заказов
    print("\n4. Тестирование заказов:")
    try:
        order_product = Product("Товар для заказа", "Описание", 75.0, 10)
        order = Order(order_product, 3)
        print(f"Создан заказ: {order}")

        # Тестирование заказа с нулевым количеством
        try:
            Order(order_product, 0)
            print("Ошибка: исключение не было вызвано")
        except ZeroQuantityError as e:
            print(f"✓ Правильно вызвано исключение для заказа: {e}")

    except ZeroQuantityError as e:
        print(f"Ошибка при создании заказа: {e}")

    print("\n=== Программа завершена ===")


if __name__ == "__main__":
    main()
