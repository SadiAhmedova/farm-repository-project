# Generated by Django 4.1.4 on 2023-08-17 11:26

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0011_alter_vegetableandfruit_photo'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='animalproduct',
            name='package',
        ),
        migrations.RemoveField(
            model_name='dairyproduct',
            name='package',
        ),
        migrations.RemoveField(
            model_name='nut',
            name='package',
        ),
    ]
