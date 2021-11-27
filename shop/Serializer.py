# coding: UTF-8
"""
Created on 2021/11/27

@author: Mark Hsu
"""
from rest_framework import serializers
from shop.models import Item, Consumer, Order


class ItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Item
        fields = ['id', 'category', 'name', 'price', 'intro', 'inventory']


class ConsumerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Consumer
        fields = ['id', 'account', 'password']


class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ['id', 'order_id', 'item', 'consumer', 'datetime']
