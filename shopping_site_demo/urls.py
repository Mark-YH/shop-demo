"""shopping_site_demo URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from shop.views import index, shop_category, shop, my_admin
from shop.api import ItemList, ItemSpecific
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    # ----- view -----
    path('django/admin/', admin.site.urls),
    path('', index),
    path('shop/<str:category>/', shop_category),
    path('shop/', shop),
    path('admin/', my_admin),
    # ----- api -----
    path('api/items/', ItemList.as_view()),
    path('api/items/<int:item_id>/', ItemSpecific.as_view()),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
