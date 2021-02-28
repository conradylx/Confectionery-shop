from django import forms
from django_countries.fields import CountryField
from django_countries.widgets import CountrySelectWidget

# PAYMENT_CHOICES = (
#     ('B', 'Blik'),
#     ('P', 'Paypal'),
#     ('D', 'Karta kredytowa'),
#     ('R', 'Przelewy')
# )


class CheckOutForm(forms.Form):
    COUNTRIES_FIRST = ['Poland']
    street_address = forms.CharField(widget=forms.TextInput(attrs={
        'placeholder': 'aleja Legionów'
    }))
    apartment_address = forms.CharField(required=False, widget=forms.TextInput(attrs={
        'placeholder': '22'
    }))
    city = forms.CharField(required=True, widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Warszawa'
    }))
    country = CountryField(blank_label='(select country)').formfield(widget=CountrySelectWidget(attrs={
        'class': 'custom-select d-block w-100',
    }))
    zip = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': '00-000'
    }))
    # payment_option = forms.ChoiceField(widget=forms.RadioSelect, choices=PAYMENT_CHOICES)
    same_billing_address = forms.BooleanField(required=False)
    save_info = forms.BooleanField(required=False)


class ContactForm(forms.Form):
    name = forms.CharField(max_length=100, error_messages=None, required=True)
    email = forms.EmailField(error_messages=None, required=True)
    phone = forms.CharField(max_length=12, error_messages=None, required=True)
    message = forms.CharField(widget=forms.Textarea, error_messages=None, required=True)