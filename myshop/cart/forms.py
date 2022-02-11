from django import forms

PRODUCT_QUANTITY_CHOICES = [(i, str(i)) for i in range(1, 21)]


class CartAddProductForm(forms.Form):
    # Кол-во товара (1-20)
    quantity = forms.TypedChoiceField(choices=PRODUCT_QUANTITY_CHOICES,
                                      coerce=int)
    # Настройка добавления товаров в корзину
    override = forms.BooleanField(required=False,
                                  initial=False,
                                  widget=forms.HiddenInput)

