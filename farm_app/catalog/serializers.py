from rest_framework import serializers
from .models import VegetableAndFruit, AnimalProduct, Nut, DairyProduct


class AnimalProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = AnimalProduct
        fields = '__all__'

class NutSerializer(serializers.ModelSerializer):
    class Meta:
        model = Nut
        fields = '__all__'

class DairyProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = DairyProduct
        fields = '__all__'


class VegetableAndFruitSerializer(serializers.ModelSerializer):
    class Meta:
        model = VegetableAndFruit
        fields = '__all__'