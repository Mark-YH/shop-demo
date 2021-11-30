from django.shortcuts import render, redirect
from shop.models import Item


# Create your views here.

def index(request):
    return redirect('/shop/')


def shop_category(request, category):
    title = str.upper(category) + ' | Shop Demo'
    items = Item.objects.filter(category=category)
    return render(request, 'shop.html', locals())


def shop(request):
    title = 'ALL | Shop Demo'
    items = Item.objects.all()
    return render(request, 'shop.html', locals())


def my_admin(request):
    return render(request, 'admin.html', locals())
