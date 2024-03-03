from cart.models import CartItem
from catalog.models import Product
from django.shortcuts import get_object_or_404
from django.http import HttpResponseRedirect
import random
import decimal

CART_ID_SESSION_KEY = 'cart_id'

# Lấy cart id của người dùng hiện tại, tạo mới nếu trống
def _cart_id(request):
    if request.session.get(CART_ID_SESSION_KEY, '') == '':
        request.session[CART_ID_SESSION_KEY] = _generate_cart_id()
    return request.session[CART_ID_SESSION_KEY]

# Tạo cart id mới
def _generate_cart_id():
    cart_id = ''
    characters = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz1234567890!@#$%^&*()'
    cart_id_length = 50
    for y in range(cart_id_length):
        cart_id += characters[random.randint(0, len(characters) - 1)]
    return cart_id

# Lấy tất cả các sản phẩm trong giỏ hàng của người dùng hiện tại
def get_cart_items(request):
    return CartItem.objects.filter(cart_id=_cart_id(request))

# Thêm một sản phẩm vào giỏ hàng
def add_to_cart(request):
    postdata = request.POST.copy()
    product_slug = postdata.get('product_slug', '')
    quantity = postdata.get('quantity', 1)
    p = get_object_or_404(Product, slug=product_slug)

    # Kiểm tra xem sản phẩm có trong giỏ hàng chưa
    cart_item = CartItem.objects.filter(cart_id=_cart_id(request), product_id=str(p.id)).first()

    if cart_item:
        # Nếu sản phẩm đã có trong giỏ hàng, tăng số lượng
        cart_item.augment_quantity(quantity)
    else:
        # Nếu sản phẩm chưa có trong giỏ hàng, tạo mới CartItem
        ci = CartItem()
        ci.product_id = str(p.id)
        ci.quantity = quantity
        ci.cart_id = _cart_id(request)
        ci.save()


# Trả về tổng số lượng các sản phẩm duy nhất trong giỏ hàng của người dùng
def cart_distinct_item_count(request):
    return get_cart_items(request).count()

def get_single_item(request, item_id):
    return get_object_or_404(CartItem, id=item_id, cart_id=_cart_id(request))

def update_cart(request):
    postdata = request.POST.copy()
    item_id = postdata['item_id']
    quantity = postdata['quantity']
    cart_item = get_single_item(request, item_id)
    if cart_item:
        if int(quantity) > 0:
            cart_item.quantity = int(quantity)
            cart_item.save()
        else:
            remove_from_cart(request)

def remove_from_cart(request):
    postdata = request.POST.copy()
    item_id = postdata['item_id']
    cart_item = get_single_item(request, item_id)
    if cart_item:
        cart_item.delete()

def cart_subtotal(request):
    cart_total = decimal.Decimal('0.00')
    cart_products = get_cart_items(request)
    
    for cart_item in cart_products:
        try:
            product = cart_item.get_product()
            # Chuyển đổi kiểu dữ liệu của product.price và cart_item.quantity sang Decimal
            price = decimal.Decimal(str(product.price))
            quantity = decimal.Decimal(str(cart_item.quantity))
            cart_total += price * quantity
        except Product.DoesNotExist:
            # Xử lý trường hợp product không tồn tại
            pass
    
    return cart_total

def is_empty(request):
    return cart_distinct_item_count(request) == 0

def empty_cart(request): 
    user_cart = get_cart_items(request) 
    user_cart.delete() 
