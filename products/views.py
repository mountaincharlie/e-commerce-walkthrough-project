from django.shortcuts import render
from .models import Product


def all_products(request):

    products = Product.objects.all()
    # data to be rendered in the html file
    context = {
        'products': products
    }

    return render(request, 'products/products.html', context)
