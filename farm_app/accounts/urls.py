from django.urls import path, include
from farm_app import settings
from django.conf.urls.static import static

from farm_app.accounts.views import ProfileLoginView, ProfileRegisterView, ProfileDetailsView, ProfileLogoutView, \
    ProfileEditView, ProfileDeleteView, error_404_view

urlpatterns = ([
path('login/', ProfileLoginView.as_view(), name='login'),
    path('register/', ProfileRegisterView.as_view(), name='register'),
    path('logout/', ProfileLogoutView.as_view(), name='logout'),

    path('<int:pk>/', include([
        path('', ProfileDetailsView.as_view(), name='profile details'),
        path('edit/', ProfileEditView.as_view(), name='profile edit'),
        path('delete/', ProfileDeleteView.as_view(), name='profile delete'),

    ])),
    path('404/', error_404_view, name= 'error'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT))
