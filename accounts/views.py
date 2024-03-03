from django.contrib.auth.forms import UserCreationForm 
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate
from checkout.models import Order, OrderItem
from accounts.forms import UserProfileForm 
# from profile import profile 
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_protect
from django.template import RequestContext
from django.http import HttpResponseRedirect

@csrf_protect
def register(request, template_name="registration/register.html"): 
    if request.method == 'POST': 
        form = UserCreationForm(request.POST)
        if form.is_valid(): 
            user = form.save()
            # Automatically log in the user after registration
            login(request, user)
            return redirect('my_account')  # Assuming you have a URL pattern named 'my_account'
    else: 
        form = UserCreationForm() 

    page_title = 'User Registration' 
    return render(request, template_name, {'form': form, 'page_title': page_title})


@login_required
def my_account(request, template_name="registration/my_account.html"):
    page_title = 'My Account'
    orders = Order.objects.filter(user=request.user)
    name = request.user.username
    return render(request, template_name, {'page_title': page_title, 'orders': orders, 'name': name})


@login_required
def order_info(request, template_name="registration/order_info.html"):
    if request.method == 'POST':
        postdata = request.POST.copy()
        form = UserProfileForm(postdata)

    #     if form.is_valid():
    #         profile.update(request)
    #         url = reverse('my_account')
    #         return HttpResponseRedirect(url)
    # else:
    #     user_profile = profile.retrieve_or_create(request)
    #     form = UserProfileForm(instance=user_profile)

    page_title = 'Edit Order Information'
    return render(request, template_name, {'form': form, 'page_title': page_title})

@login_required 
def order_details(request, order_id, template_name="registration/order_details.html"): 
    order = get_object_or_404(Order, id=order_id, user=request.user) 
    page_title = f'Order Details for Order #{order_id}' 
    order_items = OrderItem.objects.filter(order=order) 
    return render(request, template_name, {'order': order, 'order_items': order_items, 'page_title': page_title})



