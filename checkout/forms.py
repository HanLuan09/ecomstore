from django import forms
from checkout.models import Order
import datetime
import re

def cc_expire_years():
    current_year = datetime.datetime.now().year
    years = [(str(x), str(x)) for x in range(current_year, current_year + 12)]
    return years

def cc_expire_months():
    months = [(f'{month:02d}', datetime.date(2009, month, 1).strftime('%B')) for month in range(1, 13)]
    return months

CARD_TYPES = [
    ('Mastercard', 'Mastercard'),
    ('VISA', 'VISA'),
    ('AMEX', 'AMEX'),
    ('Discover', 'Discover'),
]

def strip_non_numbers(data):
    non_numbers = re.compile(r'\D')
    return non_numbers.sub('', data)

def card_luhn_checksum_is_valid(card_number):
    sum = 0
    num_digits = len(card_number)
    oddeven = num_digits & 1
    for count in range(num_digits):
        digit = int(card_number[count])
        if not ((count & 1) ^ oddeven):
            digit = digit * 2
            if digit > 9:
                digit = digit - 9
        sum += digit
    return (sum % 10) == 0

class CheckoutForm(forms.ModelForm):
    credit_card_number = forms.CharField()
    credit_card_type = forms.CharField(widget=forms.Select(choices=CARD_TYPES))
    credit_card_expire_month = forms.CharField(widget=forms.Select(choices=cc_expire_months()))
    credit_card_expire_year = forms.CharField(widget=forms.Select(choices=cc_expire_years()))
    credit_card_cvv = forms.CharField()

    class Meta:
        model = Order
        exclude = ('status', 'ip_address', 'user', 'transaction_id',)

    def __init__(self, *args, **kwargs):
        super(CheckoutForm, self).__init__(*args, **kwargs)
        self._set_widget_size()

    def _set_widget_size(self):
        size_attrs = {
            'size': '30',
            'shipping_state': '3',
            'shipping_zip': '6',
            'billing_state': '3',
            'billing_zip': '6',
            'credit_card_type': '1',
            'credit_card_expire_year': '1',
            'credit_card_expire_month': '1',
            'credit_card_cvv': '5',
        }

        for field in size_attrs:
            self.fields[field].widget.attrs['size'] = size_attrs[field]

    def clean_credit_card_number(self):
        cc_number = self.cleaned_data['credit_card_number']
        stripped_cc_number = strip_non_numbers(cc_number)
        if not card_luhn_checksum_is_valid(stripped_cc_number):
            raise forms.ValidationError('The credit card you entered is invalid.')

    def clean_phone(self):
        phone = self.cleaned_data['phone']
        stripped_phone = strip_non_numbers(phone)
        if len(stripped_phone) < 10:
            raise forms.ValidationError('Enter a valid phone number with area code (e.g., 555-555-5555).')
        return self.cleaned_data['phone']
