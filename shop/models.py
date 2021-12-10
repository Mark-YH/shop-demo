from django.db import models


# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length=50, null=False, unique=True)

    def __str__(self):
        return self.name


class Item(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='category')
    name = models.CharField(max_length=50)
    price = models.PositiveIntegerField()
    intro = models.TextField()
    inventory = models.PositiveIntegerField()

    def __str__(self):
        return self.name


class Image(models.Model):
    item = models.ForeignKey(Item, on_delete=models.CASCADE, related_name='images')
    image = models.BinaryField()

    def __str__(self):
        return str(self.image)
