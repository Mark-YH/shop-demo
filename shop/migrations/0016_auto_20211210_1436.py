# Generated by Django 3.2.9 on 2021-12-10 06:36

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0015_auto_20211208_0410'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='order',
            name='consumer',
        ),
        migrations.RemoveField(
            model_name='order',
            name='item',
        ),
        migrations.DeleteModel(
            name='Consumer',
        ),
        migrations.DeleteModel(
            name='Order',
        ),
    ]
