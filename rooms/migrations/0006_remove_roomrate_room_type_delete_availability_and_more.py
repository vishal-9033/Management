# Generated by Django 4.2.1 on 2023-05-17 12:21

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('rooms', '0005_alter_roomtype_name'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='roomrate',
            name='room_type',
        ),
        migrations.DeleteModel(
            name='Availability',
        ),
        migrations.DeleteModel(
            name='RoomRate',
        ),
    ]