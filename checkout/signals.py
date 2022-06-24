from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from .models import OrderItem


@receiver(post_save, sender=OrderItem)
def update_on_save(sender, instance, created, **kwargs):
    """
    Special function (Handles functions from the post_save event)
    sender => OrderItem
    instance => the instance of the Order that sent it
    created = > django boolean for if this is a new instance or being updated

    Reciver decorator to pass info about whats happening here
    Updates order total on orderitem update/add by applying upatde_total method
    on the instance
    """

    instance.order.update_total()


@receiver(post_delete, sender=OrderItem)
def update_on_delete(sender, instance, **kwargs):
    """
    Special function (Handles functions from the post_delete event)
    sender => OrderItem
    instance => the instance of the Order that sent it

    Reciver decorator to pass info about whats happening here
    Updates order total on orderitem delete by applying upatde_total method
    on the instance
    """

    instance.order.update_total()
