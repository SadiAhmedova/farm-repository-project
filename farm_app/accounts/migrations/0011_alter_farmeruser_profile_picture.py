# Generated by Django 4.2.11 on 2024-12-01 11:37

from django.db import migrations, models
import farm_app.catalog.validators


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0010_alter_farmeruser_groups_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='farmeruser',
            name='profile_picture',
            field=models.URLField(blank=True, max_length=500, null=True, validators=[farm_app.catalog.validators.validate_image_size]),
        ),
    ]