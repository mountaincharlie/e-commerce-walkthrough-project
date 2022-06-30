from django.db import models
from django.contrib.auth.models import User
from django_countries.fields import CountryField
from django.db.models.signals import post_save
from django.dispatch import receiver


class UserProfile(models.Model):
    """
    UserProfile class for the user to store thier delivery info
    and view their order history
    -user has a OneToOne relation with the User model
    -using the same delivery info fields we used in the Order model
    -but here all the delivery info fields should be optional
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    default_phone_number = models.CharField(
        max_length=20, null=True, blank=True
        )
    default_street_address_1 = models.CharField(
        max_length=80, null=True, blank=True
        )
    default_street_address_2 = models.CharField(
        max_length=80, null=True, blank=True
        )
    default_town_or_city = models.CharField(
        max_length=40, null=True, blank=True
        )
    default_county = models.CharField(
        max_length=80, null=True, blank=True
        )
    default_postcode = models.CharField(
        max_length=20, null=True, blank=True
        )
    default_country = CountryField(
        blank_label='Country', null=True, blank=True
        )
    

    def __str__(self):
        return self.user.username


@receiver(post_save, sender=User)
def create_or_update_user_profile(sender, instance, created, **kwargs):
    """
    Creating or updating the user's profile
    (just one signal so doesnt need it own seperate signals file)
    created = True if a new record was just created (so if the user is new)
    """
    if created:
        UserProfile.objects.create(user=instance)
    instance.userprofile.save()
