from django.contrib import admin

from .models import Product, Category


class ProductCategoryInline(admin.TabularInline):
    model = Product.categories.through


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

admin.site.register(Category, CategoryAdmin)
admin.site.register(Product, ProductAdmin)
