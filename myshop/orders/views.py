from django.shortcuts import render
from .models import OrderItem
from .forms import OrderCreateForm
from cart.cart import Cart
from .tasks import order_created


# Create your views here.


def order_create(request):
    """Работа с заказом"""
    cart = Cart(request)
    if request.method == 'POST':
        # Проверка данных, если допустимы - сохраняем
        form = OrderCreateForm(request.POST)
        if form.is_valid():
            order = form.save()
            # Запускаем асинхронную задачу
            order_created.delay(order.id)
            for item in cart:
                # Перебор всех элементов корзины и добавление в базу
                OrderItem.objects.create(order=order,
                                         product=item['product'],
                                         price=item['price'],
                                         quantity=item['quantity'])
            # Очищаем корзину
            cart.clear()
            return render(request,
                          'orders/order/created.html',
                          {'order': order})

    else:
        # Создаёт экземпляр формы
        form = OrderCreateForm()
    return render(request,
                  'orders/order/create.html',
                  {'cart': cart, 'form': form})
