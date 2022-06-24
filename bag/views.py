from django.shortcuts import render, redirect, reverse, HttpResponse, get_object_or_404
from django.contrib import messages
from products.models import Product


def view_bag(request):
    """ View to return the shopping bag page """

    context = {

    }

    return render(request, 'bag/bag.html', context)


def add_to_bag(request, item_id):
    """
    View to add a quantity of items to the shopping bag and redirect to the
    same product url
    """

    # getting the product by its pk inorder to include its name in messages
    product = get_object_or_404(Product, pk=item_id)
    # gets the value of the input with name = quantity
    quantity = int(request.POST.get('quantity'))
    #  gets url to redirect to
    redirect_url = request.POST.get('redirect_url')

    # storing the shoppin gbag in a http session so that the contents of the bag is not overwritten or lost while browsing the site until the browser is closed
    # get the var if it exists or assign empty dict
    bag = request.session.get('bag', {})

    # if that item exists in the bag already
    if item_id in list(bag.keys()):
        # adds the new quantity to existing
        bag[item_id] += quantity
        messages.success(request, f"You now have {bag[item_id]} of {product.name}'s in your bag")
    else:
        # add item_id key with quantity value to bag dict
        bag[item_id] = quantity
        messages.success(request, f'{product.name} has been added to your bag')

    # updating the bag var in the session dict
    request.session['bag'] = bag

    # to check the session thing works
    # print(request.session['bag'])

    return redirect(redirect_url)


def adjust_bag(request, item_id):
    """
    View to adjust the bag after the user makes changes to an item in their bag
    Always redirects to the shopping bag
    """

    product = get_object_or_404(Product, pk=item_id)

    # gets the value of the input with name = quantity
    quantity = int(request.POST.get('quantity'))

    # get the session if it exists or assign empty dict
    bag = request.session.get('bag', {})

    # checking if the quantity is > 0
    if quantity > 0:
        # setting the quantity value for the item_id key in bag dict
        bag[item_id] = quantity
        messages.success(request, f"You now have {bag[item_id]} of {product.name}'s in your bag")
    else:
        # otherwise removing the item entirely
        bag.pop(item_id)
        messages.success(request, f"{product.name} has been removed from your bag")

    # updating the bag var in the session dict
    request.session['bag'] = bag

    # redirects to the view_bag view
    return redirect(reverse('view_bag'))


def remove_from_bag(request, item_id):
    """
    View to remove an item from the bag if the remove button is clicked
    Dont need to get the quantity sincec they will want it to be 0
    Using a Try Except block to catch any errors since this is posted to via JS
    Always redirects to the shopping bag
    """

    product = get_object_or_404(Product, pk=item_id)

    try:
        # get the session if it exists or assign empty dict
        bag = request.session.get('bag', {})

        # removing the item from the bag dict
        bag.pop(item_id)
        messages.success(request, f"{product.name} has been removed from your bag")

        # updating the bag var in the session dict
        request.session['bag'] = bag

        # posted to via a JS function therefore need to use HttpResponse
        return HttpResponse(status=200)
    except Exception as e:
        # print(e)
        messages.error(request, f'There was an error when removing {product.name}. {e}')
        return HttpResponse(status=500)
