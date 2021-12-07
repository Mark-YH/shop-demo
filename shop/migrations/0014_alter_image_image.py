# Generated by Django 3.2.9 on 2021-12-07 12:34

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0013_alter_image_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='image',
            name='image',
            field=models.BinaryField(blank=True, editable=True, validators=[django.core.validators.validate_image_file_extension]),
        ),
    ]