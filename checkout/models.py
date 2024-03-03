from django.db import models
from django.contrib.auth.models import User
from catalog.models import Product
import decimal

class Order(models.Model):
    SUBMITTED = 1
    PROCESSED = 2
    SHIPPED = 3
    CANCELLED = 4

    ORDER_STATUSES = [
        (SUBMITTED, 'Submitted'),
        (PROCESSED, 'Processed'),
        (SHIPPED, 'Shipped'),
        (CANCELLED, 'Cancelled'),
    ]

    date = models.DateTimeField(auto_now_add=True)
    status = models.IntegerField(choices=ORDER_STATUSES, default=SUBMITTED)
    ip_address = models.GenericIPAddressField()
    last_updated = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)
    transaction_id = models.CharField(max_length=20)
    
    email = models.EmailField(max_length=50)
    phone = models.CharField(max_length=20)

    shipping_name = models.CharField(max_length=50)
    shipping_address_1 = models.CharField(max_length=50)
    shipping_address_2 = models.CharField(max_length=50, blank=True)
    shipping_city = models.CharField(max_length=50)
    shipping_state = models.CharField(max_length=2)
    shipping_country = models.CharField(max_length=50)
    shipping_zip = models.CharField(max_length=10)

    billing_name = models.CharField(max_length=50)
    billing_address_1 = models.CharField(max_length=50)
    billing_address_2 = models.CharField(max_length=50, blank=True)
    billing_city = models.CharField(max_length=50)
    billing_state = models.CharField(max_length=2)
    billing_country = models.CharField(max_length=50)
    billing_zip = models.CharField(max_length=10)

    def __str__(self):
        return 'Order #' + str(self.id)

    @property
    def total(self):
        order_items = self.orderitem_set.all()
        return sum(item.total for item in order_items)
    
    # 
    def get_absolute_url(self): 
        return ('order_details', (), { 'order_id': self.id })

class OrderItem(models.Model):
    # product = models.ForeignKey(Product, on_delete=models.CASCADE)
    product = models.CharField(max_length=24)
    quantity = models.IntegerField(default=1)
    price = models.DecimalField(max_digits=9, decimal_places=2)
    order = models.ForeignKey(Order, on_delete=models.CASCADE)

    @property
    def total(self):
        return self.quantity * self.price

    @property
    def name(self):
        return self.product.name

    @property
    def sku(self):
        return self.product.sku

    def __str__(self):
        return f"{self.product.name} ({self.product.sku})"

    def get_absolute_url(self):
        return self.product.get_absolute_url()
    

class BaseOrderInfo(models.Model):
    class Meta:
        abstract = True

    # Contact info
    email = models.EmailField(max_length=50)
    phone = models.CharField(max_length=20)

    # Shipping information
    shipping_name = models.CharField(max_length=50)
    shipping_address_1 = models.CharField(max_length=50)
    shipping_address_2 = models.CharField(max_length=50, blank=True)
    shipping_city = models.CharField(max_length=50)
    shipping_state = models.CharField(max_length=2)
    shipping_country = models.CharField(max_length=50)
    shipping_zip = models.CharField(max_length=10)

    # Billing information
    billing_name = models.CharField(max_length=50)
    billing_address_1 = models.CharField(max_length=50)
    billing_address_2 = models.CharField(max_length=50, blank=True)
    billing_city = models.CharField(max_length=50)
    billing_state = models.CharField(max_length=2)
    billing_country = models.CharField(max_length=50)
    billing_zip = models.CharField(max_length=10)

