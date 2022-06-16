from django.db import models


class Category(models.Model):
    """
    Categories for the instruments and equipment with
    programatic name and name visible to users
    """

    class Meta:
        verbose_name_plural = 'Categories'

    name = models.CharField(max_length=260)
    visible_name = models.CharField(max_length=260, null=True, blank=True)

    def __str__(self):
        return self.name

    def get_visible_name(self):
        return self.visible_name


class Product(models.Model):
    """
    Products include the instruments and equipment with
    details including:
    -category
    -sku
    -name
    -description
    -price
    -rating
    -image
    """
    category = models.ForeignKey(
        'Category', null=True, blank=True, on_delete=models.SET_NULL
        )
    sku = models.CharField(max_length=260, null=True, blank=True)
    name = models.CharField(max_length=260)
    description = models.TextField()
    price = models.DecimalField(max_digits=6, decimal_places=2)
    rating = models.DecimalField(
        max_digits=6, decimal_places=1, null=True, blank=True
        )
    image = models.ImageField(null=True, blank=True)

    def __str__(self):
        return self.name
