from django.shortcuts import render, redirect, reverse, get_object_or_404, HttpResponse
from django.views.decorators.http import require_POST
from django.contrib import messages
from django.conf import settings
from bag.contexts import bag_contents
from .forms import OrderForm
from products.models import Product
from .models import Order
from .models import OrderItem
import stripe
import json


@require_POST
def cache_checkout_data(request):
    """
    view for checking if info-save was chosen
    -gets the payment_intent id
    -sets up stripe with api key
    -call the modify method on the PaymentIntent with metadata for
    username, if they wanted to save info and a json dump of the entire bag
    """
    try:
        payment_intent_id = request.POST.get('client_secret').split('_secret')[0]
        stripe.api_key = settings.STRIPE_SECRET_KEY
        stripe.PaymentIntent.modify(payment_intent_id, metadata={
            'bag': json.dumps(request.session.get('bag', {})),
            'save_info': request.POST.get('save_info'),
            'username': request.user,
        })

        return HttpResponse(status=200)
    except Exception as e:
        messages.error(request, 'Sorry, your payment could not be processed \
            at this time please try again later')
        return HttpResponse(content=e, status=400)


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

    # checking if the method is POST
    if request.method == 'POST':
        bag = request.session.get('bag', {})

        # dict of data from the form
        form_data = {
            'full_name': request.POST['full_name'],
            'email': request.POST['email'],
            'phone_number': request.POST['phone_number'],
            'country': request.POST['country'],
            'postcode': request.POST['postcode'],
            'town_or_city': request.POST['town_or_city'],
            'street_address_1': request.POST['street_address_1'],
            'street_address_2': request.POST['street_address_2'],
            'county': request.POST['county'],
        }
        # creating the form instance
        order_form = OrderForm(form_data)
        # saving the form if its valid
        if order_form.is_valid():
            order = order_form.save(commit=False)
            payment_intent_id = request.POST.get('client_secret').split('_secret')[0]
            order.stripe_pid = payment_intent_id
            order.original_bag = json.dumps(bag)
            order.save()
            # iterating through the items to create each item in the line
            # very simialr to what we do in the context processor (make it a
            # function to be called?)
            # since bag is a dict with item_id and quantity
            for item_id, quantity in bag.items():
                try:
                    # get the item_id from the bag
                    product = Product.objects.get(id=item_id)
                    order_item = OrderItem(
                            order=order,
                            product=product,
                            quantity=quantity,
                        )
                    order_item.save()
                except Product.DoesNotExist:
                    # displaying error msg, deleting the order and redirecting
                    # to the bag
                    messages.error(request, (
                        'One of your bag items was not found in our database.'
                        'Please get in contact for assistance.'
                        ))
                    order.delete()
                    return redirect(reverse('view_bag'))

            # checking if the save info selection was made and redirecting
            request.session['save-info'] = 'save-info' in request.POST
            return redirect(reverse(
                'checkout_success', args=[order.order_number]
                ))
        else:
            # error message that the form isnt valid (they're redirected at
            # the view bottom)
            messages.error(request, (
                'There was an error with your order form.'
                ))

    # for GET method (getting the form and vars to use on the checkout page)
    else:
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


def checkout_success(request, order_number):
    """
    view to handle successful checkouts
    -takes in the request an the order_number for the order just created
    -checks if the user wanted to save their info (WILL BE USED
    AFTER USER PROFILES HAVE BEEN SETUP)
    -gets the order by its number
    -displays success msg with the order number
    -delete the bag fro mthe session
    -set template and context
    -return render
    """
    save_info = request.session.get('save-info')
    order = get_object_or_404(Order, order_number=order_number)
    messages.success(request, f'Your order was successful. Order number: {order_number}. A confirmation email will be sent to {order.email}')

    if 'bag' in request.session:
        del request.session['bag']

    template = 'checkout/checkout_success.html'
    context = {
        'order': order,
    }

    return render(request, template, context)
