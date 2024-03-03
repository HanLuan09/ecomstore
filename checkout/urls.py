from django.urls import path
from ecomstore import settings
from ecomstore.checkout.views import show_checkout, receipt

urlpatterns = [
    path('', show_checkout, {'template_name': 'checkout/checkout.html', 'SSL': settings.ENABLE_SSL }, name='checkout'),
    path('receipt/', receipt, {'template_name': 'checkout/receipt.html', 'SSL': settings.ENABLE_SSL }, name='checkout_receipt'),
]
