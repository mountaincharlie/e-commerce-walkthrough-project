from django.shortcuts import render


def view_bag(request):
    """ View to returnt he shopping bag page """

    context = {

    }

    return render(request, 'bag/bag.html', context)
