from django.contrib import admin

from . import models


class ProductCategoryInline(admin.TabularInline):
    model = models.Product.categories.through


class CategoryAdmin(admin.ModelAdmin):
    inlines = [
        ProductCategoryInline,
    ]


class ProductAdmin(admin.ModelAdmin):
    inlines = [
        ProductCategoryInline,
    ]
    list_display = ['name', 'price', 'description']
    list_filter = ['name']
    search_fields = ['name']
    exclude = ['categories']

admin.site.register(models.Category, CategoryAdmin)
admin.site.register(models.Product, ProductAdmin)
