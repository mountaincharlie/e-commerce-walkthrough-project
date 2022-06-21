from decimal import Decimal
from django.conf import settings


def bag_contents(request):
    """
    Context processor
    Returns context dictionary of data for the shopping bag
    The function is avaliable accross all the templates
    """

    # setting up vars
    bag_items = []
    total = 0
    product_count = 0

    if total < settings.FREE_DELIVERY_THRESHOLD:
        # decimal is more accurate than float for rounding
        delivery = total * Decimal(settings.STANDARD_DELIVERY_PERCENTAGE)

        # to show the user how much more they need to spend for free delivery
        free_delivery_delta = settings.FREE_DELIVERY_THRESHOLD - total
    else:
        delivery = 0
        free_delivery_delta = 0

    grand_total = total + delivery

    context = {
        'bag_items': bag_items,
        'product_count': product_count,
        'total': total,
        'delivery': delivery,
        'grand_total': grand_total,
        'free_delivery_delta': free_delivery_delta,
        'free_delivery_threshold': settings.FREE_DELIVERY_THRESHOLD,
    }

    return context
