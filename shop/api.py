# coding: UTF-8
"""
Created on 2021/11/27

@author: Mark Hsu
"""
from shop.models import Item, Image, Category
from shop.Serializer import ItemSerializer
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from django.http import Http404, HttpResponse
import PIL.Image as PImage
import copy


def save_images(request, item):
    def is_valid_image(f):
        try:
            with PImage.open(f):
                return True
        except IOError:
            return False

    response_message = {'images': []}
    files = request.FILES.getlist('images')

    PImage.init()
    for file in files:
        content_type = file.content_type.split('/')
        f = copy.deepcopy(file)
        if not (content_type[0] == 'image' and
                content_type[1].upper() in PImage.EXTENSION.values() and
                is_valid_image(f)):
            response_message['images'].append({file.name: 'Invalid file type.'})
        else:
            img = Image.objects.create(item=item, image=bytes(file.read()))
            img.save()
            response_message['images'].append({file.name: 'Successful uploaded.'})
    return response_message


def check_category(request):
    response_message = {}
    category = None
    try:
        category = Category.objects.get(name=request.data['category'])
    except Category.DoesNotExist:
        response_message.update({'category': ['Category not found.']})
    except KeyError:
        response_message.update({'category': ['This field is required.']})

    return category, response_message


class ItemList(APIView):
    def get(self, request):
        items = Item.objects.all()
        serializer = ItemSerializer(items, many=True)
        return Response(serializer.data)

    def post(self, request):
        if not request.user.is_staff:
            return Response({'Permission': 'Denied'}, status.HTTP_401_UNAUTHORIZED)

        item_serializer = ItemSerializer(data=request.data)
        category, response_message = check_category(request)

        if item_serializer.is_valid():
            if category is not None:
                item = item_serializer.save(category=category)
                response_message.update(dict(item_serializer.data))
                response_message.update(save_images(request, item))
            return Response(response_message, status=status.HTTP_201_CREATED)
        response_message.update(item_serializer.errors)
        return Response(response_message, status=status.HTTP_400_BAD_REQUEST)


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
        if not request.user.is_staff:
            return Response({'Permission': 'Denied'}, status.HTTP_401_UNAUTHORIZED)
        item = self.get_object(item_id)
        serializer = ItemSerializer(item, data=request.data, partial=True)
        if serializer.is_valid():
            category, msg = check_category(request)
            if category is None:
                serializer.save()
            else:
                serializer.save(category=category)
            response_message = dict(serializer.data)
            response_message.update(save_images(request, item))
            if msg:
                response_message.update(msg)
            return Response(response_message)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, item_id):
        if not request.user.is_staff:
            return Response({'Permission': 'Denied'}, status.HTTP_401_UNAUTHORIZED)
        item = self.get_object(item_id)
        item.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class ImageSpecific(APIView):
    def get(self, request, image_id):
        image = Image.objects.get(id=image_id)
        return HttpResponse(bytes(image.image), content_type='image/png')

    def delete(self, request, image_id):
        if not request.user.is_staff:
            return Response({'Permission': 'Denied'}, status.HTTP_401_UNAUTHORIZED)
        image = Image.objects.get(id=image_id)
        image.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
