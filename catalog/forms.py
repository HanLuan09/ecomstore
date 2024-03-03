from django import forms
from cart.models import CartItem
from catalog.models import Product

class ProductAdminForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = '__all__'
    def clean_price(self):
        if self.cleaned_data['price'] <= 0:
            raise forms.ValidationError('Price must be greater than zero.')
        return self.cleaned_data['price']
    
    def save(self, commit=True):
        using_db = 'mongodb'
        instance = super().save(commit=False)
        
        if commit:
            instance.save(using=using_db)
            
        return instance

class ProductAddToCartForm(forms.Form):
    quantity = forms.IntegerField(
        widget=forms.TextInput(attrs={'size': '2', 'value': '1', 'class': 'quantity', 'maxlength': '5'}),
        error_messages={'invalid': 'Please enter a valid quantity.'},
        min_value=1
    )
    product_slug = forms.CharField(widget=forms.HiddenInput())

    # ghi đè hàm __init__ mặc định để có thể đặt request
    def __init__(self, request=None, *args, **kwargs):
        self.request = request
        super(ProductAddToCartForm, self).__init__(*args, **kwargs)

    # kiểm tra cookie tùy chỉnh
    def clean(self):
        if self.request:
            if not self.request.session.test_cookie_worked():
                raise forms.ValidationError("Cookies must be enabled.")
        return self.cleaned_data
