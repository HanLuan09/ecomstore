from django.shortcuts import render, get_object_or_404, render_to_response
from django.http import HttpResponseRedirect
from django.template import RequestContext
from django.contrib.auth.decorators import login_required
from checkout import checkout
from ecomstore import settings
from checkout.models import Order, OrderItem
from cart import cart
from accounts import profile
from checkout.forms import CheckoutForm 

@login_required
def show_cart(request, template_name):
    if request.method == 'POST':
        postdata = request.POST.copy()
        
        if 'submit' in postdata:
            if postdata['submit'] == 'Remove':
                cart.remove_from_cart(request)
            elif postdata['submit'] == 'Update':
                cart.update_cart(request)
            elif postdata['submit'] == 'Checkout':
                checkout_url = checkout.get_checkout_url(request)
                return HttpResponseRedirect(checkout_url)

    cart_items = cart.get_cart_items(request)
    page_title = 'Shopping Cart'
    cart_subtotal = cart.cart_subtotal(request)

    # for Google Checkout button
    merchant_id = settings.GOOGLE_CHECKOUT_MERCHANT_ID

    return render(request, template_name, locals())

@login_required 
def show_checkout(request, template_name="checkout/checkout.html"):
    if request.method == 'POST':
        # Handle POST request logic
        pass
    else:
        if request.user.is_authenticated:
            user_profile = profile.retrieve(request)
            form = CheckoutForm(instance=user_profile)
        else:
            form = CheckoutForm()
        
        page_title = 'Checkout'
        return render(request, template_name, {'form': form, 'page_title': page_title})
