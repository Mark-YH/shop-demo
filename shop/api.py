# coding: UTF-8
"""
Created on 2021/11/27

@author: Mark Hsu
"""
from shop.models import Consumer, Item, Order, Image
from shop.Serializer import OrderSerializer, ConsumerSerializer, ItemSerializer, ImageSerializer
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from django.http import Http404
from django.conf import settings
import os


def save_images(request, item_id, response_msg):
    query_dict = request.data.copy()
    query_dict.update({'item': item_id})  # `item[0]` is the latest item.

    response_msg.update({'images': []})
    files = request.FILES.getlist('images')
    for file in files:
        query_dict['image'] = file
        img_serializer = ImageSerializer(data=query_dict)
        if img_serializer.is_valid():
            img_serializer.save()
            response_msg['images'].append(dict(img_serializer.data))
        else:
            response_msg['images'].append(dict(img_serializer.errors))
    return response_msg


class ItemList(APIView):
    def get(self, request):
        items = Item.objects.all()
        serializer = ItemSerializer(items, many=True)
        return Response(serializer.data)

    def post(self, request):
        item_serializer = ItemSerializer(data=request.data)
        if item_serializer.is_valid():
            item_serializer.save()

            # The following filter is equivalent to SQL schema:
            # select * from "shop_item"
            # where name='data['name']' and intro='data['intro']'
            # order by id desc limit 1;
            item = Item.objects.filter(
                name=item_serializer.data['name'],
                intro=item_serializer.data['intro']
            ).order_by('-id')[:1]

            response_message = save_images(request, item[0].id, dict(item_serializer.data.items()))
            return Response(response_message, status=status.HTTP_201_CREATED)
        return Response(item_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ItemSpecific(APIView):
    def get_object(self, item_id):
        try:
            return Item.objects.get(id=item_id)
        except Item.DoesNotExist:
            raise Http404

    def get(self, request, item_id):
        item = self.get_object(item_id)
        serializer = ItemSerializer(item)
        return Response(serializer.data)

    def put(self, request, item_id):
        item = self.get_object(item_id)
        serializer = ItemSerializer(item, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            response_message = save_images(request, item.id, dict(serializer.data.items()))
            return Response(response_message)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, item_id):
        images = Image.objects.filter(item_id=item_id)
        for img in images:
            try:
                os.remove(os.path.join(settings.BASE_DIR, img.image.path))
            except FileNotFoundError:
                continue
        item = self.get_object(item_id)
        item.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class ImageSpecific(APIView):
    def delete(self, request, img):
        image = Image.objects.get(image=img.replace('-*slash*-', '/'))
        image.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
