# Generated by Django 3.2 on 2021-08-25 05:06

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ceuApp', '0002_auto_20210825_0353'),
    ]

    operations = [
        migrations.RenameField(
            model_name='user',
            old_name='first_name',
            new_name='fname',
        ),
        migrations.RenameField(
            model_name='user',
            old_name='last_name',
            new_name='lname',
        ),
    ]
