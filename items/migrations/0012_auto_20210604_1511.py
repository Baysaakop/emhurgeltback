# Generated by Django 3.1.4 on 2021-06-04 07:11

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('items', '0011_auto_20210604_1501'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='district',
            name='city',
        ),
        migrations.RemoveField(
            model_name='shop',
            name='address',
        ),
        migrations.DeleteModel(
            name='Address',
        ),
        migrations.DeleteModel(
            name='City',
        ),
        migrations.DeleteModel(
            name='District',
        ),
    ]
