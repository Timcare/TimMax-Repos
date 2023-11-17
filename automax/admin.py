from django.contrib import admin
from .models import Listing,LinkedListing

# Register your models here.
@admin.register(Listing)
class ListingAdmin(admin.ModelAdmin):
    readonly_fields=("id",)
    list_display=("id",'created_at')

@admin.register(LinkedListing)
class LinkedListinggAdmin(admin.ModelAdmin):
    pass