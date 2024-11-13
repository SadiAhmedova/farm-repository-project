from datetime import date

from django import forms
from django.contrib.auth import forms as auth_forms, get_user_model

from farm_app.accounts.models import FarmerUser
from farm_app.common.helpers import BootstrapFormMixin
from farm_app.catalog.models import VegetableAndFruit


class CreateProfileForm(auth_forms.UserCreationForm):
    password1 = forms.CharField(
        label="Password",
        widget=forms.PasswordInput(
            attrs={'class': 'form-field', 'type': 'password'}),
    )
    password2 = forms.CharField(
        label="Confirm password",
        widget=forms.PasswordInput(
            attrs={'class': 'form-field', 'type': 'password'}),
    )

    class Meta(auth_forms.UserCreationForm.Meta):
        model = FarmerUser
        fields = ('first_name', 'last_name', 'username','gender', 'date_of_birth', 'email','profile_picture', 'password1', 'password2')

        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-field', 'required': True}),
            'last_name': forms.TextInput(attrs={'class': 'form-field', 'required': True}),
            'username': forms.TextInput(attrs={'class': 'form-field', 'required': True}),
            'gender': forms.Select(attrs={'class': 'form-field'}),
            'email': forms.EmailInput(attrs={'class': 'form-field'}),
            'date_of_birth': forms.DateInput(attrs={'class':'form-field', 'type':'date','max':date.today(), 'required': True})
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['password1'].help_text = None
        self.fields['password2'].help_text = None


class LoginProfileForm(auth_forms.AuthenticationForm):
    username = auth_forms.UsernameField(
        widget=forms.TextInput(
            attrs={"autofocus": True,
                   "class": 'form-field', }))
    password = forms.CharField(
        strip=False,
        widget=forms.PasswordInput(
            attrs={"autocomplete": "current-password",
                   "class": 'form-field', }),
    )


class EditProfileForm(forms.ModelForm):
    class Meta:
        model = FarmerUser
        fields = ['username', 'first_name', 'last_name', 'email', 'date_of_birth', 'gender', 'profile_picture']
        widgets = {
            'username': forms.TextInput(
                attrs={
                    'class': 'form-field',
                }
            ),
            'first_name': forms.TextInput(
                attrs={
                    'class': 'form-field',
                }
            ),
            'last_name': forms.TextInput(
                attrs={
                    'class': 'form-field',
                }
            ),
            'email': forms.EmailInput(
                attrs={
                    'class': 'form-field',
                }
            ),

            'date_of_birth': forms.DateInput(
                attrs={
                    'class': 'form-field',
                    'type':'date', 'max': date.today()
                }
            ),
            'gender': forms.Select(
                attrs={
                    'class': 'form-field',
                }
            ),

        }
