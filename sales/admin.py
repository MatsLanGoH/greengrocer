from django.contrib import admin

# Register your models here.
from .models import Fruit


# Register the Admin classes for Fruit using the decorator
@admin.register(Fruit)
class FruitAdmin(admin.ModelAdmin):
    list_display = ('id', 'label', 'price', 'created_at', 'updated_at')
    list_filter = ('label', 'price')



