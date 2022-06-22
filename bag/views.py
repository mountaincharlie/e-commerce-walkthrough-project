from django.shortcuts import render, redirect


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
    else:
        # add item_id key with quantity value to bag dict
        bag[item_id] = quantity

    # updating the bag var in the session dict
    request.session['bag'] = bag

    # to check the session thing works
    # print(request.session['bag'])

    return redirect(redirect_url)
