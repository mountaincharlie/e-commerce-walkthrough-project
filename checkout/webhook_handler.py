from django.http import HttpResponse


# creating a custom class
class StripeWH_Handler:
    """ Handling Stripe webhooks """

    def __init__(self, request):
        """ sets up the class """
        self.request = request

    def handle_event(self, event):
        """
        Handles any webhook event sent from Stripe
        """
        return HttpResponse(
            content=f'Webhook recieved: {event["type"]}',
            status=200
        )
