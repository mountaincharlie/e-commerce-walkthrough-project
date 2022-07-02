from decimal import Decimal
from django.conf import settings
from django.shortcuts import get_object_or_404
from products.models import Product


def bag_contents(request):
    """
    Context processor
    Returns context dictionary of data for the shopping bag
    The function is avaliable accross all the templates
    """

    # setting up vars
    # list of dicts containing item_id, quantitiy and the product obj
    bag_items = []
    total = 0
    product_count = 0
    # get the var if it exists or assign empty dict
    bag = request.session.get('bag', {})

    # using bag items to calc the total, items and product_count
    # item_id is the key and quantity is its value
    for item_id, quantity in bag.items():
        # checks that the item is not found for the bag if its been deleted
        if Product.objects.filter(pk=item_id).exists():
            # get the product
            product = Product.objects.get(pk=item_id)
            total += quantity * product.price
            product_count += quantity
            bag_items.append({
                'item_id': item_id,
                'quantity': quantity,
                'product': product,
                'sub_total': (product.price * quantity)
            })

    if total < settings.FREE_DELIVERY_THRESHOLD:
        # decimal is more accurate than float for rounding
        delivery = total * Decimal(settings.STANDARD_DELIVERY_PERCENTAGE / 100)

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
