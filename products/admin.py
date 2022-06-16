from django.contrib import admin
from .models import Product, Category


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):

    list_display = (
        'sku',
        'name',
        'category',
        'price',
        'rating',
        'image',
        'description',
    )

    ordering = ('sku',)

    search_fields = (
        'name',
        'category',
        'description',
    )

    list_filter = (
        'category',
        'price',
        'rating',
    )

    # actions = any methods you want to define below


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):

    list_display = (
        'visible_name',
        'name',
        'pk',
    )

    ordering = ('visible_name',)

    search_fields = (
        'visible_name',
        'name',
    )

    # actions = any methods you want to define below
