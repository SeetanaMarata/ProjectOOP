from .abstract_models import BaseContainer
from .exceptions import ZeroQuantityError
from .models import Product


class Order(BaseContainer):
    """Класс для представления заказа."""

    def __init__(self, product: Product, quantity: int):
        """
        Инициализация заказа.

        Args:
            product: Товар в заказе
            quantity: Количество товара

        Raises:
            ZeroQuantityError: Если количество равно нулю
        """
        if quantity == 0:
            raise ZeroQuantityError("Нельзя создать заказ с нулевым количеством товара")

        self.product = product
        self.quantity = quantity
        self.total_price = product.price * quantity

    def __repr__(self) -> str:
        return f"Order(product={self.product.name!r}, quantity={self.quantity}, total_price={self.total_price})"

    def __str__(self) -> str:
        return f"Заказ: {self.product.name}, количество: {self.quantity}, итого: {self.total_price} руб."
