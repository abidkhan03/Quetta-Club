from django import forms
from .models import Customers

class CustomersForm(forms.Form):
    customer_name = forms.CharField(max_length=25)
    customer_rank = forms.CharField(max_length=20)
    customer_id = forms.CharField(max_length=10)
    customer_file = forms.FileField(required=False)

    class Meta:
        model = Customers
        fields = ('customer_name', 'customer_rank', 'customer_id', 'customer_file')