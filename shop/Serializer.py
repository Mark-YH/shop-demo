# coding: UTF-8
"""
Created on 2021/11/27

@author: Mark Hsu
"""
from rest_framework import serializers
from shop.models import Item, Image


class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Image
        fields = ['id', 'image']


class ItemSerializer(serializers.ModelSerializer):
    images = ImageSerializer(many=True, required=False)
    category = serializers.StringRelatedField()

    class Meta:
        model = Item
        fields = ['id', 'category', 'name', 'price', 'intro', 'inventory', 'images']
