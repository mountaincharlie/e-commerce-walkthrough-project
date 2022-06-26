from django.shortcuts import render, redirect, reverse
from django.contrib import messages
from .forms import OrderForm


def checkout(request):
    """
    -gets the bag from the session
    -if there is nothing in the bag an error message is displayed and the
    user is redirected to the products page
    -stores an instance of the OrderForm
    -defines the template to use
    -defines the context dict with the OrderForm to be accessed within
    the template
    """
    bag = request.session.get('bag', {})

    if not bag:
        messages.error(request, 'There are currently no items in your bag')
        return redirect(reverse('products'))

    order_form = OrderForm()
    template = 'checkout/checkout.html'
    context = {
        'order_form': order_form,
        'stripe_public_key': 'pk_test_51LEzH6E9H0YubpCH5C6h02DovtSzaRVuvwwlLJlYssn5sXorwl2DM5LjGvZ751akqzMil1O8WjFghkERWQFInuYS00KOM40tWM',
        'client_secret': 'test client secret',
    }

    return render(request, template, context)
