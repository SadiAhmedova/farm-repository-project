# Generated by Django 4.1.4 on 2023-11-25 08:29

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0017_alter_animalproduct_options_and_more'),
        ('order', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='orderitem',
            name='dairy',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='DairyProduct', to='catalog.dairyproduct'),
        ),
        migrations.AlterField(
            model_name='orderitem',
            name='fruit',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='VegetableAndFruit', to='catalog.vegetableandfruit'),
        ),
        migrations.AlterField(
            model_name='orderitem',
            name='meat',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='AnimalProduct', to='catalog.animalproduct'),
        ),
        migrations.AlterField(
            model_name='orderitem',
            name='nut',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='Nut', to='catalog.nut'),
        ),
    ]
