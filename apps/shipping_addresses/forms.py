from django.forms import ModelForm
from .models import Shipping_address

class ShippingAddressForm(ModelForm):
    class Meta:
        model = Shipping_address
        fields = [
            'line1',
            'line2',
            'city',
            'state',
            'country',
            'postal_code',
            'reference'
        ]
        labels = {
            'line1':'Calle 1',
            'line2':'Calle 2',
            'city':'Ciudad',
            'state':'Región',
            'country':'País',
            'postal_code':'Código postal',
            'reference':'Referencias'
        }
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['line1'].widget.attrs.update({'class':'form-control'})
        self.fields['line2'].widget.attrs.update({'class': 'form-control'})
        self.fields['city'].widget.attrs.update({'class': 'form-control'})
        self.fields['state'].widget.attrs.update({'class': 'form-control'})
        self.fields['country'].widget.attrs.update({'class': 'form-control'})
        self.fields['postal_code'].widget.attrs.update({'class': 'form-control', 'placeholder':'0000'})
        self.fields['reference'].widget.attrs.update({'class': 'form-control'})
