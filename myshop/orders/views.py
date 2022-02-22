from django.urls import reverse
from django.shortcuts import render, redirect
from .models import OrderItem
from .forms import OrderCreateForm
from cart.cart import Cart
from sendmail.views import contact_view


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
            contact_view.delay(order.id)
            # Установим порядок в сеансе
            request.session['order_id'] = order.id
            # Перенаправление на оплату
            return redirect(reverse('payment:process'))
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
