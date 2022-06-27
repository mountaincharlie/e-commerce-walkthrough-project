from django.http import HttpResponse


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
        return HttpResponse(
            content=f'Webhook recieved: {event["type"]}',
            status=200
        )

    def handle_payment_intent_payment_failed(self, event):
        """
        Handles payment_intent.payment_failed webhook from Stripe
        Used each time the user completes the payment process
        unsuccessfully
        """
        return HttpResponse(
            content=f'Webhook recieved: {event["type"]}',
            status=200
        )
