from django.shortcuts import render
from shop.models import Item


# Create your views here.

def index(request):
    title = 'Shop Demo'
    return render(request, 'index.html', locals())


def shop(request, category):
    title = str.upper(category) + ' | Shop Demo'
    items = Item.objects.filter(category=category)
    return render(request, 'shop.html', locals())


def my_admin(request):
    return render(request, 'admin.html', locals())
