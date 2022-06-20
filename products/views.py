from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.contrib import messages
from django.db.models import Q
from .models import Product


def all_products(request):
    """
    view for rendering the products.html template with all the products
    """

    products = Product.objects.all()
    query = None  # to prevent errors when query is empty

    # handling GET requests
    if request.GET:
        # if query (name attribute) exists, we need to get its value
        if 'query' in request.GET:
            query = request.GET['query']
            # handling blank search with django message and redirect
            if not query:
                messages.error(request, 'Your search was empty')
                # reverse here just reloads the page
                return redirect(reverse('products'))

            # using Django's Q to check if the search is in title OR desc
            queries = Q(name__icontains=query) | Q(description__icontains=query)
            products = products.filter(queries)

    # data to be rendered in the html file
    context = {
        'products': products,
        'product_search': query,
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
