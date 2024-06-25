from django import forms
from .models import ShippingAddress

class ShippingAddressForm(forms.ModelForm):
    shipping_full_name = forms.CharField(label= '', widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Inter your Full name'}), required=True)
    shipping_email = forms.CharField(label= '', widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Inter your email'}), required=True)
    shipping_phone = forms.CharField(label= '', widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Inter your phone number'}), required=True)    
    shipping_address1 = forms.CharField(label= '', widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Inter your address '}), required=True)
    shipping_address2 = forms.CharField(label= '', widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Inter another address (optional)'}), required=False)
    shipping_country = forms.CharField(label= '', widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Inter your country '}), required=True)
    shipping_city = forms.CharField(label= '', widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Inter your city '}), required=True)
    shipping_state = forms.CharField(label= '', widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Inter your state '}), required=True)

    class Meta:

        model = ShippingAddress
        fields = ['shipping_full_name', 'shipping_email', 'shipping_address1', 'shipping_address2', 'shipping_country', 'shipping_city', 'shipping_state', 'shipping_phone']

        exclude = ['user',]


class BillingForm(forms.Form):

    card_name = forms.CharField(label= '', widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Inter your name (on a card)'}), required=True)
    card_num = forms.CharField(label= '', widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Inter your card number'}), required=True)
    card_expiration_date = forms.CharField(label= '', widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':' Expiration date '}), required=True)
    card_CVV = forms.CharField(label= '', widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'CVV code'}), required=False)
