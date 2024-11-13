import datetime
from enum import Enum

from django.core.exceptions import ValidationError
from django.utils import timezone
from django.utils.safestring import mark_safe
from rest_framework import serializers
from django.db import models

from farm_app.accounts.validators import validate_only_letter_value
from farm_app.catalog.validators import validate_image_size

UserModel = 'accounts.FarmerUser'


class ChoicesMixin:
    @classmethod
    def choice(cls):
        return [(choice.value, choice.name) for choice in cls]


class ChoicesLengthMixin(ChoicesMixin):
    @classmethod
    def max_length(cls):
        return max(len(ch.value) for ch in cls)

class VegFruitChoice(ChoicesLengthMixin, Enum):
    CARROT = 'Carrot'
    POTATO = 'Potato'
    CABBAGE = 'Cabbage'
    CAULIFLOWER = 'Cauliflower'
    CUCUMBERS = 'Cucumber'
    TOMATO = 'Tomato'
    ONION = 'Onion'
    BROCCOLI = 'Broccoli'
    EGGPLANT = 'Eggplant'
    PEPPER = 'Pepper'
    CORN = 'Corn'
    PUMPKIN = 'Pumpkin'
    APPLE = 'Apple'
    GRAPE = 'Grape'
    STRAWBERRY = 'Strawberry'
    PEAR = 'Pear'
    PLUM = 'Plum'
    ORANGE = 'Orange'
    CHERRY = 'Cherry'
    BLACKBERRY = 'Blackberry'
    LEMON = 'Lemon'
    PEACH = 'Peach'
    MELON = 'Melon'
    WATERMELON = 'Watermelon'
    OTHER = 'Other'


class DairyChoice(ChoicesLengthMixin, Enum):
    MILK = 'Milk'
    BUTTER = 'Butter'
    CHEESE = 'Cheese'
    CURD = 'Curd'
    YOGURT = 'Yogurt'
    OTHER = 'Other'


class AnimalChoice(ChoicesLengthMixin, Enum):
    CHICKEN = 'Chicken'
    PIG = 'Pig'
    COW = 'Cow'
    GOAT = 'Goat'
    SHEEP = 'Sheep'
    TURKEY = 'Turkey'
    GOOSE = 'Goose'
    RABBIT = 'Rabbit'
    HORSE = 'Horse'
    DONKEY = 'Donkey'
    LAMB = 'Lamb'
    OTHER = 'Other'


class NutChoices(ChoicesLengthMixin, Enum):
    ROASTED = 'Roasted'
    RAW = 'Raw'
    DRIED_FRUIT = 'Dried'
    OTHER = 'Other'


class VegetableAndFruit(models.Model):
    MAX_LENGTH_OF_PRODUCTION_COUNTRY = 40

    name = models.CharField(choices=VegFruitChoice.choice(),
                            max_length=VegFruitChoice.max_length(),
                            default=VegFruitChoice.OTHER.value)

    price = models.FloatField()
    production = models.CharField(null=True, blank=True, max_length=MAX_LENGTH_OF_PRODUCTION_COUNTRY,
                                  validators=[validate_only_letter_value])

    photo = models.ImageField(upload_to='uploads/', blank=True, null=True, validators=(validate_image_size,))

    user = models.ForeignKey(
        UserModel,
        on_delete=models.CASCADE,
    )

    def clean(self):
        if len(self.name) > 15:
            raise ValidationError(
                {'name': "Name should have less than 15 letters"})
        elif len(self.name) <= 2:
            raise ValidationError(
                {'name': "Name should have at least 3 letters"})
        if len(self.production) > 15:
            raise ValidationError(
                {'name': "Production should have less than 15 letters"})
        elif len(self.production) <= 2:
            raise ValidationError(
                {'name': "Production should have at least 3 letters"})

    def to_json(self):
        return '{"name": "%s"}' % self.name

    def __str__(self):
        return f'{self.name}'

    class Meta:
        ordering = ['-price']


class DairyProduct(models.Model):
    MAX_LENGTH_OF_PACKAGE = 100
    name = models.CharField(choices=DairyChoice.choice(),
                            max_length=DairyChoice.max_length(),
                            default=DairyChoice.OTHER.value)
    percent = models.FloatField(null=True, blank=True)
    price = models.FloatField()
    photo = models.ImageField(upload_to='uploads/', blank=True, null=True, validators=(validate_image_size,))

    user = models.ForeignKey(
        UserModel,
        on_delete=models.CASCADE,
    )

    def clean(self):
        if len(self.name) > 15:
            raise ValidationError(
                {'name': "Name should have less than 15 letters"})
        elif len(self.name) <= 2:
            raise ValidationError(
                {'name': "Name should have at least 3 letters"})

    def to_json(self):
        return '{"name": "%s"}' % self.name

    def __str__(self):
        if self.percent:
            return f'{self.name} {self.percent}%'
        return f'{self.name}'

    class Meta:
        ordering = ['-price']


class AnimalProduct(models.Model):
    MAX_LENGTH_OF_PRODUCTION_COUNTRY = 40
    PRODUCT_MAX_LENGTH = 40

    type = models.CharField(choices=AnimalChoice.choice(),
                            max_length=AnimalChoice.max_length(),
                            default=AnimalChoice.OTHER.value)
    name = models.CharField(
        max_length=PRODUCT_MAX_LENGTH, validators=[validate_only_letter_value]
    )
    price = models.FloatField()
    photo = models.ImageField(upload_to='uploads/', blank=True, null=True, validators=(validate_image_size,))
    date_of_birth = models.DateField(null=True, blank=True)

    production = models.CharField(null=True, blank=True, max_length=MAX_LENGTH_OF_PRODUCTION_COUNTRY,
                                  validators=[validate_only_letter_value])
    user = models.ForeignKey(
        UserModel,
        on_delete=models.CASCADE,
    )

    @property
    def age(self):
        return datetime.datetime.now().year - self.date_of_birth.year

    def clean(self):
        if len(self.name) > 15:
            raise ValidationError(
                {'name': "Name should have less than 15 letters"})
        elif len(self.name) <= 2:
            raise ValidationError(
                {'name': "Name should have at least 3 letters"})
        if len(self.production) > 15:
            raise ValidationError(
                {'name': "Production should have less than 15 letters"})
        elif len(self.production) <= 2:
            raise ValidationError(
                {'name': "Production should have at least 3 letters"})

    def to_json(self):
        return '{"name": "%s"}' % self.name

    def __str__(self):
        return f'{self.name} from {self.type}'

    class Meta:
        ordering = ['-price']


class Nut(models.Model):
    NUTS_MAX_LENGTH = 35

    type = models.CharField(choices=NutChoices.choice(),
                            max_length=NutChoices.max_length(),
                            default=NutChoices.OTHER.value)

    name = models.CharField(
        max_length=NUTS_MAX_LENGTH, validators=[validate_only_letter_value]
    )
    price = models.FloatField()
    photo = models.ImageField(upload_to='uploads/', blank=True, null=True, validators=(validate_image_size,))

    user = models.ForeignKey(
        UserModel,
        on_delete=models.CASCADE,
    )

    def clean(self):
        if len(self.name) > 15:
            raise ValidationError(
                {'name': "Name should have less than 15 letters"})
        if len(self.name) <= 2:
            raise ValidationError(
                {'name': "Name should have at least 3 letters"})

    def to_json(self):
        return '{"name": "%s"}' % self.name

    def __str__(self):
        return f'{self.type} {self.name}'

    class Meta:
        ordering = ['-price']
