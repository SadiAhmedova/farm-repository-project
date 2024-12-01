from django.contrib import admin
from django.contrib.auth import get_user_model

from farm_app.accounts.models import  FarmerUser

UserModel = 'accounts.FarmerUser'
@admin.register(FarmerUser)
class FarmerUserAdmin(admin.ModelAdmin):
    list_display = ('username','first_name', 'last_name', 'date_of_birth',)
    search_fields = ('username', 'first_name',)
    list_filter = ('date_of_birth',)