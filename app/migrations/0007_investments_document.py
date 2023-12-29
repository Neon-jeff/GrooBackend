# Generated by Django 5.0 on 2023-12-27 05:42

import cloudinary.models
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0006_rename_reciept_investments_image'),
    ]

    operations = [
        migrations.AddField(
            model_name='investments',
            name='document',
            field=cloudinary.models.CloudinaryField(blank=True, max_length=255, null=True, verbose_name='file'),
        ),
    ]