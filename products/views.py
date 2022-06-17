from django.shortcuts import render, get_object_or_404
from .models import Product


def all_products(request):
    """
    view for rendering the products.html template with all the products
    """

    products = Product.objects.all()
    # data to be rendered in the html file
    context = {
        'products': products
    }

    return render(request, 'products/products.html', context)


def product_details(request, product_id):
    """
    view for rendering the product_details.html template with
    all the product's details, using its id in the url
    """

    product = get_object_or_404(Product, pk=product_id)
    # data to be rendered in the html file
    context = {
        'product': product
    }

    return render(request, 'products/product_details.html', context)
