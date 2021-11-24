from django.shortcuts import render


# Create your views here.

def index(request):
    title = 'Shop Demo'
    return render(request, 'index.html', locals())


def shop(request, category):
    title = str.upper(category) + ' | Shop Demo'
    item_id = 1
    name = 'T-shirt'
    price = 100
    intro = 'This is ...'
    inventory = 5
    img = '/static/media/' + category + '/' + str(item_id) + '.png'
    return render(request, 'shop.html', locals())
