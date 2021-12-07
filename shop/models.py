from django.db import models
from django.core import validators


# Create your models here.

class Item(models.Model):
    category = models.CharField(max_length=50)
    name = models.CharField(max_length=50)
    price = models.PositiveIntegerField()
    intro = models.TextField()
    inventory = models.PositiveIntegerField()

    def __str__(self):
        return self.name


class Consumer(models.Model):
    account = models.CharField(max_length=50, unique=True, validators=[validators.EmailValidator])
    password = models.CharField(max_length=512)

    def __str__(self):
        return self.account


class Order(models.Model):
    order_id = models.PositiveIntegerField()
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    consumer = models.ForeignKey(Consumer, on_delete=models.CASCADE)
    datetime = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.order_id)


class Image(models.Model):
    item = models.ForeignKey(Item, on_delete=models.CASCADE, related_name='image_set')
    image = models.BinaryField(blank=True, editable=True, validators=[validators.validate_image_file_extension])

    def __str__(self):
        return str(self.image)
