from django.shortcuts import render, get_object_or_404
from django.contrib import messages
from .models import UserProfile
from .forms import UserProfileForm
from checkout.models import Order


def profile(request):
    """ view for displaying the user's profile """

    user_profile = get_object_or_404(UserProfile, user=request.user)

    # handling POST requests when the form is submitted
    if request.method == 'POST':
        # create anew instance of the user profile
        form = UserProfileForm(request.POST, instance=user_profile)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated succesfully!')
        else:
            messages.error(
                request, 'Your details could not be updated right now. Please try again later'
                )
            # form = UserProfileForm()
    else:
        # form with the user's details pre-populated
        form = UserProfileForm(instance=user_profile)

    # getting the user's orders history
    orders = user_profile.orders.all()

    template = 'profiles/profile.html'
    context = {
        'form': form,
        'orders': orders,
        'on_profile_page': True,
    }

    return render(request, template, context)


def order_history(request, order_number):
    """
    view for displaying the order history for a particular
    order by its order_number
    """

    # gets the order
    order = get_object_or_404(Order, order_number=order_number)

    # informing the user whats happening
    messages.info(request, (
        f'This is the confirmation details of your past order, order_number: {order_number}'
        f'A confirmation email was sent on {order.date}'
    ))

    # uses the checkout_success template to display the info
    template = 'checkout/checkout_success.html'
    context = {
        'order': order,
        'from_profile': True,  # to confirm they got to the url from the profile page
    }

    return render(request, template, context)
