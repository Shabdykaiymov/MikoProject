# listings/admin.py
from django.contrib import admin
from .models import Category, Listing

class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)

class ListingAdmin(admin.ModelAdmin):
    list_display = ('title', 'price', 'category', 'user', 'created_at')
    list_filter = ('category', 'created_at')
    search_fields = ('title', 'description')
    readonly_fields = ('created_at', 'updated_at')

admin.site.register(Category, CategoryAdmin)
admin.site.register(Listing, ListingAdmin)