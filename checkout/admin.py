from django.contrib import admin
from .models import Order, OrderItem


class OrderItemAdminInline(admin.TabularInline):
    """
    Inline table for each item in the order
    Allows adding/editing order items in the admin from inside the Order model
    """

    model = OrderItem
    readonly_fields = ('orderitem_total',)


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    """
    inlines => the inline we want to add (OrderItemAdminInline)
    readonly_fields => fields auto generated and therefore shouldnt be edited
    fields => all of our fields in the same ordering as in the model
    list_diaply => columns you want to see in the admin view
    ordering => by most recent created date
    """

    inlines = (OrderItemAdminInline,)

    readonly_fields = (
        'order_number',
        'date',
        'delivery_cost',
        'order_total',
        'grand_total',
        'original_bag',
        'stripe_pid',
    )

    fields = (
        'order_number',
        'user_profile',
        'date',
        'full_name',
        'email',
        'phone_number',
        'country',
        'postcode',
        'town_or_city',
        'street_address_1',
        'street_address_2',
        'county',
        'delivery_cost',
        'order_total',
        'grand_total',
        'original_bag',
        'stripe_pid',
    )

    list_display = (
        'order_number',
        'date',
        'full_name',
        'order_total',
        'delivery_cost',
        'grand_total',
    )

    ordering = ('-date',)
