from django.urls import path
from . import views

app_name = 'payment'

urlpatterns = [
    path('process/', views.payment_process, name='process'),  # Обработка платежа
    path('done/', views.payment_done, name='done'),  # Перенаправление пользователя в случае успешного платежа
    path('canceled/', views.payment_canceled, name='canceled'),  # Перенаправление пользователя если платёж не удался
]
