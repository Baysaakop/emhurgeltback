# Generated by Django 3.1.4 on 2021-09-17 03:56

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('items', '0001_initial'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Category',
            new_name='Type',
        ),
        migrations.RemoveField(
            model_name='item',
            name='category',
        ),
    ]
