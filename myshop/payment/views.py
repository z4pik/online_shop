import braintree
from django.shortcuts import render, redirect, get_object_or_404
from django.conf import settings
from orders.models import Order

# Создание экземлпяра платёжного шлюза Braintree
gateway = braintree.BraintreeGateway(settings.BRAINTREE_CONF)


def payment_process(request):
    """
    Управляет процессом выписки
    """
    # Получаем id заказа которые хранили в сеансе
    order_id = request.session.get('order_id')
    order = get_object_or_404(Order, id=order_id)
    total_cost = order.get_total_cost()

    if request.method == 'POST':
        # Получаем nonce
        nonce = request.POST.get('payment_method_nonce', None)
        # Создаём и отправляем транзакцию
        result = gateway.transaction.sale({
            'amount': f'{total_cost:.2f}',  # Общая стоимость заказа
            'payment_method_nonce': nonce,  # Токен nonce
            'options': {  # Отправляем транзакцию сразу на расчёт
                'submit_for_settlement': True
            }
        })
        if result.is_success:
            # Помечаем заказ как оплаченный
            order.paid = True
            # Сохраняем идентификатор транзакции
            order.braintree_id = result.transaction.id
            order.save()
            # Запускаем ассинхронную задачу

            return redirect('payment:done')
        else:
            # Если платёж не удалася
            return redirect('payment:canceled')
    # Если представление было загруженно с запросом GET
    else:
        # Создаём токен
        client_token = gateway.client_token.generate()
        return render(request,
                      'payment/process.html',
                      {'order': order,
                       'client_token': client_token})


def payment_done(request):
    """ Когда платёж был успешен"""
    return render(request, 'payment/done.html')


def payment_canceled(request):
    """ Когда платёж не был успешен"""
    return render(request, 'payment/canceled.html')
