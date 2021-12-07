from django.contrib import admin
from shop.models import Item, Consumer, Order, Image, Category

# Register your models here.
admin.site.register(Item)
admin.site.register(Consumer)
admin.site.register(Order)
admin.site.register(Image)
admin.site.register(Category)
