from django.shortcuts import render, get_object_or_404
from django.contrib import messages
from .models import UserProfile
from .forms import UserProfileForm


def profile(request):
    """ view for displaying the user's profile """

    user_profile = get_object_or_404(UserProfile, user=request.user)

    # handling POST requests when the form is submitted
    if request.method == 'POST':
        # create anew instance of the user profile
        form = UserProfileForm(request.POST, instance=user_profile)
        if form.is_valid():
            print('form is valid')
            form.save()
            messages.success(request, 'Profile updated succesfully!')
        else:
            messages.error(request, 'Your details could not be updated right now. Please try again later')
            form = UserProfileForm(instance=user_profile)

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
