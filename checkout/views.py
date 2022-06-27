from django.shortcuts import render, redirect, reverse
from django.contrib import messages
from django.conf import settings
from bag.contexts import bag_contents
from .forms import OrderForm
import stripe


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

    # stripe vars
    stripe_public_key = settings.STRIPE_PUBLIC_KEY
    stripe_secret_key = settings.STRIPE_SECRET_KEY

    bag = request.session.get('bag', {})

    if not bag:
        messages.error(request, 'There are currently no items in your bag')
        return redirect(reverse('products'))

    current_bag = bag_contents(request)
    grand_total = current_bag['grand_total']
    stripe_total = round(grand_total * 100)  # stripe needs it as an int
    stripe.api_key = stripe_secret_key
    # creating the PaymentIntent (dict of details about the payment)
    payment_intent = stripe.PaymentIntent.create(
        amount=stripe_total,
        currency=settings.STRIPE_CURRENCY,
    )

    # print(payment_intent)

    order_form = OrderForm()

    # just a message for if you have to set the var every time
    if not stripe_public_key:
        messages.warning(request, 'Stripe public key is missing. Did you set it in your enviroment?')

    template = 'checkout/checkout.html'

    # conatins form, the public key for stripe and the payment intent's secret
    context = {
        'order_form': order_form,
        'stripe_public_key': stripe_public_key,
        'client_secret': payment_intent.client_secret,
    }

    return render(request, template, context)
