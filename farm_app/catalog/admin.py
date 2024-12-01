from django.contrib import admin

# Register your models here.
from farm_app.catalog.models import VegetableAndFruit, DairyProduct, AnimalProduct, Nut


@admin.register(VegetableAndFruit)
class VegetableAndFruitAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'user',)
    search_fields = ('name', 'user',)
    list_filter = ('price',)

@admin.register(DairyProduct)
class DairyProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'percent', 'price', 'user',)
    search_fields = ('name', 'user',)
    list_filter = ('price',)

@admin.register(AnimalProduct)
class AnimalProductAdmin(admin.ModelAdmin):
    list_display = ('type','name', 'price', 'user',)
    search_fields = ('type','name', 'user',)
    list_filter = ('price',)

@admin.register(Nut)
class Nut(admin.ModelAdmin):
    list_display = ('name', 'price', 'user',)
    search_fields = ('name', 'user',)
    list_filter = ('price',)


