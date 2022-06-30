from django.http import HttpResponse
from .models import Order, OrderItem
from products.models import Product
from profiles.models import UserProfile
import json
import time


# creating a custom class
class StripeWH_Handler:
    """ Handling Stripe webhooks """

    def __init__(self, request):
        """ sets up the class """
        self.request = request

    def handle_event(self, event):
        """
        Handles non-specific webhook event sent from Stripe
        """
        return HttpResponse(
            content=f'Unhandled webhook recieved: {event["type"]}',
            status=200
        )

    def handle_payment_intent_succeeded(self, event):
        """
        Handles payment_intent.succeeded webhook from Stripe
        Used each time the user completes the payment process
        successfully
        """
        # getting the intent and extracting the variables we need from it
        intent = event.data.object
        payment_intent_id = intent.payment_intent_id
        bag = intent.metadata.bag
        save_info = intent.metadata.save_info

        # storing billing/shipping details/grand_total
        billing_details = intent.charges.data[0].billing_details
        shipping_details = intent.shipping
        grand_total = round(intent.charges.data[0].amount / 100, 2)

        # replace empty strings with none to fit format in db
        for field, value in shipping_details.address.items():
            if value == '':
                shipping_details.address[field] = None

        # update the user profile
        profile = None  # so that it still works for anonymous users
        username = intent.metadata.username
        # checking if the user is authenticated (can use request.user.is_authenticated aswell)
        if username != 'AnonymousUser':
            profile = UserProfile.objects.get(user__username=username)
            if save_info:
                profile.default_phone_number = shipping_details.phone
                profile.default_country = shipping_details.address.country
                profile.default_postcode = shipping_details.address.postal_code
                profile.default_town_or_city = shipping_details.address.city
                profile.default_street_address_1 = shipping_details.address.line1
                profile.default_street_address_2 = shipping_details.address.line2
                profile.default_county = shipping_details.address.state
                profile.save()

        # ---- checking if the order already exists (was successful)
        order_exists = False
        attempt = 1
        while attempt <= 5:
            try:
                # finding the order
                order = Order.objects.get(
                    full_name__iexact=shipping_details.name,
                    email__iexact=billing_details.email,
                    phone_number__iexact=shipping_details.phone,
                    country__iexact=shipping_details.address.country,
                    postcode__iexact=shipping_details.address.postal_code,
                    town_or_city__iexact=shipping_details.address.city,
                    street_address_1__iexact=shipping_details.address.line1,
                    street_address_2__iexact=shipping_details.address.line2,
                    county__iexact=shipping_details.address.state,
                    grand_total=grand_total,
                    original_bag=bag,
                    stripe_pid=payment_intent_id,
                )
                order_exists = True
                # breaking from the loop if found
                break
            # if the order hasnt been found yet/doesnt exist
            except Order.DoesNotExist:
                # incrementing attempts if not found yet
                attempt += 1
                time.sleep(1)
        if order_exists:
            # http response
            return HttpResponse(
                content=f'Webhook recieved: {event["type"]} | SUCCESS: Verified order already in database',
                status=200)
        else:
            order = None
            try:
                # creating the order
                order = Order.objects.create(
                    full_name=shipping_details.name,
                    user_profile=profile,
                    email=billing_details.email,
                    phone_number=shipping_details.phone,
                    country=shipping_details.address.country,
                    postcode=shipping_details.address.postal_code,
                    town_or_city=shipping_details.address.city,
                    street_address_1=shipping_details.address.line1,
                    street_address_2=shipping_details.address.line2,
                    county=shipping_details.address.state,
                    original_bag=bag,
                    stripe_pid=payment_intent_id,
                )
                # copied from views DOES THIS WORK?
                for item_id, quantity in json.loads(bag).items():
                    # get the item_id from the bag
                    product = Product.objects.get(id=item_id)
                    order_item = OrderItem(
                        order=order,
                        product=product,
                        quantity=quantity,
                    )
                    order_item.save()
            except Exception as e:
                # delete order if it exists
                if order:
                    order.delete()
                return HttpResponse(
                    content=f'Webhook recieved: {event["type"]} | ERROR: {e}', status=500)

        return HttpResponse(
            content=f'Webhook recieved: {event["type"]} | SUCCESS: Created order in webhook',
            status=200)

    def handle_payment_intent_payment_failed(self, event):
        """
        Handles payment_intent.payment_failed webhook from Stripe
        Used each time the user completes the payment process
        unsuccessfully
        """
        return HttpResponse(
            content=f'Webhook recieved: {event["type"]}',
            status=200)
