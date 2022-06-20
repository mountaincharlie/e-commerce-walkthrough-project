from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.contrib import messages
from django.db.models import Q
from .models import Product, Category


def all_products(request):
    """
    view for rendering the products.html template with all the products
    This view also filters the products by different search results,
    catgeories and orderings
    """

    products = Product.objects.all()  # gets all the products first
    query = None  # to prevent errors when query is empty
    categories = None

    # handling GET requests
    if request.GET:

        # handling category selections
        if 'category' in request.GET:
            # get list of categories and filtering the products which contain these
            categories = request.GET['category'].split(',')
            # here we specify 'category' model before 'name' since it has FK relation to 'product'
            products = products.filter(category__name__in=categories)
            # to get a list of actual category objects
            categories = Category.objects.filter(name__in=categories)

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
        'search_categories': categories,
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
