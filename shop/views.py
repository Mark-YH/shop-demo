from django.shortcuts import render, redirect
from shop.models import Item, Category
from django.contrib import auth
from django.contrib.auth.models import User
import base64
import json
from googleoauth.auth_manager import GoogleAccountManager

ga_manager = GoogleAccountManager()

def get_authorization(user):
    return user.is_authenticated, user.is_staff


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
        for image in item_obj.images.all():
            items[i]['images'].append({
                'id': image.id,
                'image': base64.b64encode(bytes(image.image))
            })
    return items


def index(request):
    return redirect('/shop/')


def shop_category(request, category):
    title = str.upper(category) + ' | Shop Demo'
    items_obj = Item.objects.filter(category=Category.objects.get(name=category))
    items = get_items_dict(items_obj)
    is_login, is_admin = get_authorization(request.user)
    return render(request, 'shop.html', locals())


def shop(request):
    title = 'ALL | Shop Demo'
    items_obj = Item.objects.all()
    items = get_items_dict(items_obj)
    is_login, is_admin = get_authorization(request.user)
    return render(request, 'shop.html', locals())


def details(request, item_id):
    item_obj = Item.objects.get(id=item_id)
    item = get_items_dict([item_obj])[0]
    title = item['name'] + ' | Shop Demo'
    is_login, is_admin = get_authorization(request.user)
    return render(request, 'details.html', locals())


def my_admin(request):
    is_login, is_admin = get_authorization(request.user)
    if is_login and is_admin:
        return render(request, 'admin.html', locals())
    else:
        return redirect('/shop/')


def get_acc_pwd(payload):
    try:
        acc = payload['account']
        pwd = payload['password']
    except KeyError:
        acc = None
        pwd = None
    return acc, pwd


def login(request):
    if request.user.is_authenticated:
        return redirect('/shop/')

    if request.method == 'POST':
        account, password = get_acc_pwd(request.POST)

        if account is None and password is None:
            msg = 'Login failed'
            render(request, 'login.html', locals())

        user = auth.authenticate(username=account, password=password)
        if user is not None:
            auth.login(request, user=user)  # 建立 session
            return redirect('/shop/')
        else:
            msg = 'Invalid account or password.'
    return render(request, 'login.html', locals())


def logout(request):
    auth.logout(request)
    return redirect('/shop/')


def register(request):
    if request.method == 'POST':
        account, password = get_acc_pwd(request.POST)
        if password != request.POST['password_confirm']:
            msg = '密碼輸入錯誤'
            return render(request, 'register.html', locals())
        try:
            User.objects.get(username=account)
            msg = '帳號已存在'
            return render(request, 'register.html', locals())
        except User.DoesNotExist as e:
            user = User.objects.create_user(username=account, password=password)
            auth.login(request, user=user)
            return redirect('/shop/')
    return render(request, 'register.html', locals())


def cart_view(request):
    def get_item(item_id):
        try:
            return Item.objects.get(id=item_id)
        except Item.DoesNotExist:
            return None

    def post():
        msg = '謝謝惠顧'
        for key in request.POST:
            if 'amount' in key:
                item_id = key.split('-')[1]
                item = get_item(item_id)
                if item.inventory >= int(request.POST[key]):
                    item.inventory -= int(request.POST[key])
                    item.save()
                else:
                    msg = '商品數量不足'
                    return render(request, 'cart.html', locals())
        response = render(request, 'cart.html', locals())
        response.delete_cookie('cart')
        return response

    def get():
        msg = ''
        cart = request.COOKIES['cart']
        cart = json.loads(cart)
        item_list = []
        for k, v in cart.items():
            item = get_item(k)
            if item is not None:
                amount = v if item.inventory > v else item.inventory
                item_list.append({'id': item.id, 'name': item.name, 'amount': amount, 'price': item.price * amount})

        total_price = sum([it['price'] for it in item_list])
        return render(request, 'cart.html', locals())

    if 'cart' not in request.COOKIES:
        msg = '目前沒有任何商品'
        return render(request, 'cart.html', locals())

    if request.method == 'POST':
        return post()
    else:
        return get()


def google_login(request):
    if request.user.is_authenticated:
        return redirect('/shop/')
    return ga_manager.login(request)


def authorize(request):
    response = ga_manager.authorize(request)
    return response


def oauth2callback(request):
    return ga_manager.callback(request)
