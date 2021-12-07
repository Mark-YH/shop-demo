from django.shortcuts import render, redirect
from shop.models import Item
import base64


# Create your views here.

def index(request):
    return redirect('/shop/')


def get_items_dict(items_obj):
    items = []
    for i, item_obj in enumerate(items_obj):
        items.append({
            'id': item_obj.id,
            'name': item_obj.name,
            'price': item_obj.price,
            'inventory': item_obj.inventory,
            'intro': item_obj.intro,
            'images': [],
        })
        for image in item_obj.image_set.all():
            items[i]['images'].append({
                'id': image.id,
                'image': base64.b64encode(bytes(image.image))
            })
    return items


def shop_category(request, category):
    title = str.upper(category) + ' | Shop Demo'
    items_obj = Item.objects.filter(category=category)
    items = get_items_dict(items_obj)
    return render(request, 'shop.html', locals())


def shop(request):
    title = 'ALL | Shop Demo'
    items_obj = Item.objects.all()
    items = get_items_dict(items_obj)
    return render(request, 'shop.html', locals())


def my_admin(request):
    return render(request, 'admin.html', locals())
