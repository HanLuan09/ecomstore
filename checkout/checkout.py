from checkout import google_checkout 
from checkout import authnet
from cart import cart
from checkout.models import Order, OrderItem
from checkout.forms import CheckoutForm
from accounts import profile 

def get_checkout_url(request): 
    return google_checkout.get_checkout_url(request)

def process(request):
    # Transaction results
    APPROVED = '1'
    DECLINED = '2'
    ERROR = '3'
    HELD_FOR_REVIEW = '4'

    postdata = request.POST.copy()
    card_num = postdata.get('credit_card_number', '')
    exp_month = postdata.get('credit_card_expire_month', '')
    exp_year = postdata.get('credit_card_expire_year', '')
    exp_date = exp_month + exp_year
    cvv = postdata.get('credit_card_cvv', '')
    amount = cart.cart_subtotal(request)
    results = {}

    response = authnet.do_auth_capture(
        amount=amount,
        card_num=card_num,
        exp_date=exp_date,
        card_cvv=cvv
    )

    if response[0] == APPROVED:
        transaction_id = response[6]
        order = create_order(request, transaction_id)
        results = {'order_number': order.id, 'message': ''}
    elif response[0] == DECLINED:
        results = {'order_number': 0, 'message': 'There is a problem with your credit card.'}
    elif response[0] == ERROR or response[0] == HELD_FOR_REVIEW:
        results = {'order_number': 0, 'message': 'Error processing your order.'}

    return results

def create_order(request, transaction_id):
    order = Order()
    order.user = None 
    if request.user.is_authenticated(): 
        order.user = request.user 
        
    checkout_form = CheckoutForm(request.POST, instance=order)
    order = checkout_form.save(commit=False)
    order.transaction_id = transaction_id
    order.ip_address = request.META.get('REMOTE_ADDR')
    order.user = None
    order.status = Order.SUBMITTED
    order.save()

    # If the order save succeeded
    if order.pk:
        cart_items = cart.get_cart_items(request)
        for ci in cart_items:
            # Create order item for each cart item
            oi = OrderItem()
            oi.order = order
            oi.quantity = ci.quantity
            oi.price = ci.price  # Now using @property
            oi.product = ci.product
            oi.save()

        # All set, empty cart
        cart.empty_cart(request)
        if request.user.is_authenticated(): 
            profile.set(request) 
        # return the new order object 
        return order 
