from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.contrib import messages
from django.db.models import Q
from django.db.models.functions import Lower
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
    sort = None
    direction = None

    # handling GET requests
    if request.GET:

        # checking if sorting has been applied first
        if 'sort' in request.GET:
            sort_key = request.GET['sort']
            sort = sort_key  # sent to context?
            # using 'annotation' to add temporary field to model
            if sort_key == 'name':
                sort_key = 'lower_name'
                products = products.annotate(lower_name=Lower('name'))
            if sort_key == 'category':
                # setting the products to order by category name if category is the sorting criteria
                sort_key = 'category__name'
            if 'direction' in request.GET:
                direction = request.GET['direction']
                # check if its decending so you add a '-' before
                if direction == 'desc':
                    sort_key = f'-{sort_key}'

            # ordering the products
            products = products.order_by(sort_key)


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

    # defining the current sorting 
    current_sorting = f'{sort}_{direction}'
    # data to be rendered in the html file
    context = {
        'products': products,
        'product_search': query,
        'search_categories': categories,
        'sort_parameters': current_sorting,
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
