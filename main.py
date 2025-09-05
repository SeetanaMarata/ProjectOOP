"""
Основной модуль приложения для управления товарами и категориями.
"""

from src.ecommerce.models import Category, LawnGrass, Product, Smartphone
from src.ecommerce.orders import Order


def main() -> None:
    """Основная функция приложения."""
    print("=== E-Commerce Management System ===")

    # Сброс счетчиков для чистого теста
    Category.category_count = 0
    Category.product_count = 0

    # Создаем тестовые данные
    print("\n1. Создание тестовых товаров и категорий:")

    # Создаем товары разных типов (будет выведена информация о создании благодаря миксину)
    product1 = Product("Наушники", "Беспроводные наушники", 199.99, 20)
    smartphone1 = Smartphone(
        "iPhone 15", "Смартфон Apple", 999.99, 10, "Высокая", "15 Pro", 256, "Black"
    )
    smartphone2 = Smartphone(
        "Samsung Galaxy", "Смартфон Samsung", 799.99, 15, "Высокая", "S23", 128, "White"
    )
    lawn_grass1 = LawnGrass(
        "Газонная трава Premium",
        "Качественная трава",
        49.99,
        100,
        "Германия",
        14,
        "Зеленый",
    )

    # Создаем категории
    electronics = Category(
        "Электроника", "Электронные устройства", [product1, smartphone1, smartphone2]
    )
    garden = Category("Сад", "Товары для сада", [lawn_grass1])

    # Демонстрация создания заказов
    print("\n2. Создание заказов:")
    order1 = Order(smartphone1, 2)
    order2 = Order(lawn_grass1, 10)

    print(f"Создан заказ: {order1}")
    print(f"Создан заказ: {order2}")

    # Демонстрация сложения товаров одного класса
    print("\n3. Демонстрация сложения товаров одного класса:")
    try:
        total_smartphones = smartphone1 + smartphone2
        print(f"Общая стоимость смартфонов: {total_smartphones:.2f} руб.")
    except TypeError as e:
        print(f"Ошибка: {e}")

    # Демонстрация ошибки при сложении товаров разных классов
    print("\n4. Демонстрация ошибки при сложении разных классов:")
    try:
        invalid_total = smartphone1 + lawn_grass1
        print(f"Результат: {invalid_total:.2f} руб.")
    except TypeError as e:
        print(f"Ожидаемая ошибка: {e}")

    # Показываем статистику
    print("\n5. Статистика:")
    print(f"Всего категорий: {Category.category_count}")
    print(f"Всего товаров: {Category.product_count}")

    # Демонстрация итерации по товарам
    print("\n6. Товары в категории 'Электроника':")
    for product in electronics:
        print(f"  - {product}")

    print("\n7. Товары в категории 'Сад':")
    for product in garden:
        print(f"  - {product}")

    print("\n=== Программа завершена ===")


if __name__ == "__main__":
    main()
