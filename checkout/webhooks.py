from django.conf import settings
from django.http import HttpResponse
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt
from checkout.webhook_handler import StripeWH_Handler
import stripe


@require_POST
@csrf_exempt
def webhook(request):
    """ Listens for webhooks from Stripe """

    # Setup api key and wh_secret
    wh_secret = settings.STRIPE_WH_SECRET
    stripe.api_key = settings.STRIPE_SECRET_KEY

    # Get the webhook data and verify its signature
    payload = request.body
    sig_header = request.META['HTTP_STRIPE_SIGNATURE']
    event = None

    # try to create the event
    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, wh_secret
        )
    except ValueError as e:
        # Invalid payload
        return HttpResponse(status=400)
    except stripe.error.SignatureVerificationError as e:
        # Invalid signature
        return HttpResponse(status=400)
    except Exception as e:
        # generic exception handler
        return HttpResponse(content=e, status=400)

    # for testing the view works
    # print('success!')
    # return HttpResponse(status=200)

    # setting up an instance of the webhook handler with request
    handler = StripeWH_Handler(request)

    # event map dict to map webhook events to the required handler functions
    event_map = {
        'payment_intent.succeeded': handler.handle_payment_intent_succeeded,
        'payment_intent.payment_failed': handler.handle_payment_intent_payment_failed,
    }

    # getting the webhook's type from Stripe
    event_type = event['type']

    # gets the required handler if it exists, else uses the generic one
    event_handler = event_map.get(event_type, handler.handle_event)

    # calling the event handler with the event
    response = event_handler(event)
    return response
