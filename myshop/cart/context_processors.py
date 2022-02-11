"""
    Создаём экземпляр корзины с помощью объекта запроса и делаем её
    доступной в виде переменной 'cart'
"""
from .cart import Cart


def cart(request):
    return {'cart': Cart(request)}
