from django import forms
from django_countries.fields import CountryField
from django_countries.widgets import CountrySelectWidget

PAYMENT_CHOICES = (
    ('S', 'Stripe'),
    ('P', 'Paypal')
)


class CheckOutForm(forms.Form):
    street_address = forms.CharField(widget=forms.TextInput(attrs={
        'placeholder': '1234 Street'
    }))
    apartment_address = forms.CharField(required=False, widget=forms.TextInput(attrs={
        'placeholder': '2000/22'
    }))
    city = forms.CharField(required=True, widget=forms.TextInput(attrs={
        'class': 'form-control'
    }))
    country = CountryField(blank_label='(select country)').formfield(widget=CountrySelectWidget(attrs={
        'class':'custom-select d-block w-100'
    }))
    zip = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control'
    }))
    same_billing_address = forms.BooleanField(required=False)
    save_info = forms.BooleanField(required=False)
    payment_option = forms.ChoiceField(
        widget=forms.RadioSelect, choices=PAYMENT_CHOICES)


class ContactForm(forms.Form):
    name = forms.CharField(max_length=100, error_messages=None, required=True)
    email = forms.EmailField(error_messages=None, required=True)
    phone = forms.CharField(max_length=12, error_messages=None, required=True)
    message = forms.CharField(widget=forms.Textarea, error_messages=None, required=True)