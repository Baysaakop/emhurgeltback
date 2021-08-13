# Generated by Django 3.1.4 on 2021-08-13 05:49

from django.db import migrations, models
import items.models


class Migration(migrations.Migration):

    dependencies = [
        ('items', '0022_tag_name_en'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='item',
            name='images',
        ),
        migrations.AddField(
            model_name='item',
            name='image1',
            field=models.ImageField(blank=True, null=True, upload_to=items.models.item_directory_path),
        ),
        migrations.AddField(
            model_name='item',
            name='image2',
            field=models.ImageField(blank=True, null=True, upload_to=items.models.item_directory_path),
        ),
        migrations.AddField(
            model_name='item',
            name='image3',
            field=models.ImageField(blank=True, null=True, upload_to=items.models.item_directory_path),
        ),
        migrations.AddField(
            model_name='item',
            name='image4',
            field=models.ImageField(blank=True, null=True, upload_to=items.models.item_directory_path),
        ),
        migrations.DeleteModel(
            name='ItemImage',
        ),
    ]
