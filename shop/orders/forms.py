from django import forms

from .models import Order


class OrderCreateForm(forms.ModelForm):
    postal_code = forms.DecimalField()

    class Meta:
        model = Order
        fields = ['first_name', 'last_name', 'email', 'address',
                  'postal_code', 'city']
