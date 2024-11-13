from enum import Enum

from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.db import models

from farm_app.accounts.validators import validate_only_letter_value
from farm_app.catalog.models import ChoicesLengthMixin
from farm_app.catalog.validators import validate_image_size


class Gender(ChoicesLengthMixin, Enum):
    MALE = 'Male'
    FEMALE = 'Female'
    DO_NOT_SHOW = 'Do Not Show'

class FarmerUser(AbstractUser):
    USERNAME_MAX_LENGTH = 30

    FIRST_NAME_MAX_LENGTH = 25
    LAST_NAME_MAX_LENGTH = 25

    username = models.CharField(
        max_length=USERNAME_MAX_LENGTH,
        unique=True,
    )
    first_name = models.CharField(null=True,blank=True,max_length=FIRST_NAME_MAX_LENGTH, validators=[validate_only_letter_value])

    last_name = models.CharField(null=True,blank=True,max_length=LAST_NAME_MAX_LENGTH, validators=[validate_only_letter_value])

    email =models.EmailField()
    profile_picture = models.ImageField(upload_to='uploads/', blank=True, null=True, validators=(validate_image_size,))
    date_of_birth = models.DateField(null=True, blank=True)
    gender = models.CharField(choices=Gender.choice(),
                              max_length=Gender.max_length(),
                              default=Gender.DO_NOT_SHOW.value)

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    def get_user_name(self):
        if self.first_name and self.last_name:
            return self.first_name + ' ' + self.last_name
        elif self.first_name or self.last_name:
            return self.first_name or self.last_name
        else:
            return self.username

    def clean(self):
        if len(self.first_name) > 25:
            raise ValidationError(
                {'first_name': "First name should have less than 15 letters"})
        elif len(self.first_name) < 2:
            raise ValidationError(
                {'first_name': "First name should have at least 2 letters"})

        if len(self.last_name) > 25:
            raise ValidationError(
                {'last_name': "Last name should have less than 15 letters"})
        elif len(self.first_name) < 2:
            raise ValidationError(
                {'last_name': "Last name should have at least 2 letters"})


    class Meta:
        ordering = ['-date_of_birth', 'username']


# class Profile(models.Model):
#     FIRST_NAME_MIN_LENGTH = 2
#     FIRST_NAME_MAX_LENGTH = 25
#     LAST_NAME_MIN_LENGTH = 2
#     LAST_NAME_MAX_LENGTH = 25
#
#     VEG_FRUIT = 'Vegetables and Fruits'
#     DAIRY = 'Dairy products'
#     ANIMAL = 'Animal products'
#     NUTS = 'Nuts'
#
#     PRODUCTION_VARIETY = [(production, production) for production in (VEG_FRUIT, DAIRY, ANIMAL, NUTS)]
#
#     DO_NOT_SHOW = 'Do not show'
#     MALE = 'Male'
#     FEMALE = 'Female'
#
#     GENDER_CHOICES = [(x, x) for x in (DO_NOT_SHOW, MALE, FEMALE)]
#
#     first_name = models.CharField(
#         max_length=FIRST_NAME_MAX_LENGTH,
#         validators=(
#             MinLengthValidator(FIRST_NAME_MIN_LENGTH),
#         ),
#     )
#
#     last_name = models.CharField(
#         max_length=LAST_NAME_MAX_LENGTH,
#         validators=(
#             MinLengthValidator(LAST_NAME_MIN_LENGTH),
#         ),
#     )
#
#     picture = models.FileField()
#
#     date_of_birth = models.DateField(
#         null=True,
#         blank=True,
#     )
#
#     email = models.EmailField(
#         null=True,
#         blank=True,
#     )
#
#     gender = models.CharField(
#         max_length=max(len(x) for (x, _) in GENDER_CHOICES),
#         choices=GENDER_CHOICES,
#         null=True,
#         blank=True,
#         default=DO_NOT_SHOW,
#     )
#
#
#     user = models.OneToOneField(
#         FarmerUser,
#         on_delete=models.CASCADE,
#         primary_key=True,
#     )
#
#     def __str__(self):
#         return f'{self.first_name} {self.last_name}'
