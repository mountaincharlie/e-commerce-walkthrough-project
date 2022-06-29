import uuid  # for generating the order numbers
from django.db import models
from django.db.models import Sum
from django.conf import settings
from django_countries.fields import CountryField
from products.models import Product


class Order(models.Model):
    """ The whole order in the users bag """

    # it will be auto generated and unique
    order_number = models.CharField(max_length=32, null=False, editable=False)
    full_name = models.CharField(max_length=50, null=False, blank=False)
    email = models.EmailField(max_length=254, null=False, blank=False)
    phone_number = models.CharField(max_length=20, null=False, blank=False)
    country = CountryField(blank_label='Country *', null=False, blank=False)
    postcode = models.CharField(max_length=20, null=True, blank=True)
    town_or_city = models.CharField(max_length=40, null=False, blank=False)
    street_address_1 = models.CharField(max_length=80, null=False, blank=False)
    street_address_2 = models.CharField(max_length=80, null=True, blank=True)
    county = models.CharField(max_length=80, null=True, blank=True)
    date = models.DateTimeField(auto_now_add=True)
    delivery_cost = models.DecimalField(
        max_digits=6, decimal_places=2, null=False, default=0
        )
    order_total = models.DecimalField(
        max_digits=10, decimal_places=2, null=False, default=0
        )
    grand_total = models.DecimalField(
        max_digits=10, decimal_places=2, null=False, default=0
        )
    original_bag = models.TextField(null=False, blank=False, default='')
    stripe_pid = models.CharField(
        max_length=254, null=False, blank=False, default=''
        )

    def _generate_order_number(self):
        """
        Generates random unique 32 digit order number with uuid
        Prepended with _ to indicate its only used in this class
        """
        return uuid.uuid4().hex.upper()

    def update_total(self):
        """
        Updates the grand total everytime a new item is added to the order
        Uses the 'orderitems' related_name
        Accounts for delivery cost by checking if the threshold has been reached
        """

        self.order_total = self.orderitems.aggregate(
            Sum('orderitem_total')
            )['orderitem_total__sum'] or 0

        if self.order_total < settings.FREE_DELIVERY_THRESHOLD:
            self.delivery_cost = self.order_total * settings.STANDARD_DELIVERY_PERCENTAGE / 100
        else:
            self.delivery_cost = 0
        
        self.grand_total = self.order_total + self.delivery_cost
        self.save()  # saves the instance

    def save(self, *agrs, **kwargs):
        """
        Overrides save method
        Sets order number if it doesnt already have one
        Calls the save method again
        """
        if not self.order_number:
            self.order_number = self._generate_order_number()
        super().save(*agrs, **kwargs)

    def __str__(self):
        """ Returns the order_number """
        return self.order_number


class OrderItem(models.Model):
    """ Each item in the order """

    order = models.ForeignKey(Order, null=False, blank=False, on_delete=models.CASCADE, related_name='orderitems')
    product = models.ForeignKey(Product, null=False, blank=False, on_delete=models.CASCADE)
    quantity = models.IntegerField(null=False, blank=False, default=0)
    orderitem_total = models.DecimalField(max_digits=6, decimal_places=2,  null=False, blank=False, editable=False)  # it will be auto generated on save

    def save(self, *agrs, **kwargs):
        """
        Overrides save method
        Sets orderitem_total
        Updates order total
        Applies save method
        """
        self.orderitem_total = self.product.price * self.quantity
        super().save(*agrs, **kwargs)

    def __str__(self):
        """ Returns the item sku and order_number it belongs to """
        return f'SKU {self.product.sku} on order {self.order.order_number}'
