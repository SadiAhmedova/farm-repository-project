from django.conf.urls.static import static
from django.urls import path, include

from farm_app import settings
from farm_app.catalog import views as views

urlpatterns = ([
    path('', views.IndexView.as_view(), name='home'),
    path('vegetable/add/', views.VegetableCreateView.as_view(), name='add vegetable'),
    path('vegetable/<int:pk>/', include([
        path('', views.VegetableDetailsView.as_view(), name='details vegetable'),
        path('edit/', views.VegetableEditView.as_view(), name='edit vegetable'),
        path('delete/', views.VegetableDeleteView.as_view(), name='delete vegetable'),
    ])),
    path('nut/add/', views.NutCreateView.as_view(), name='add nut'),
    path('nut/<int:pk>/', include([
        path('', views.NutDetailsView.as_view(), name='details nut'),
        path('edit/', views.NutEditView.as_view(), name='edit nut'),
        path('delete/', views.NutDeleteView.as_view(), name='delete nut'),
    ])),
    path('dairy/add/', views.DairyCreateView.as_view(), name='add dairy'),
    path('dairy/<int:pk>/', include([
        path('', views.DairyDetailsView.as_view(), name='details dairy'),
        path('edit/', views.DairyEditView.as_view(), name='edit dairy'),
        path('delete/', views.DairyDeleteView.as_view(), name='delete dairy'),
    ])),
    path('animal/add/', views.AnimalCreateView.as_view(), name='add animal'),
    path('animal/<int:pk>/', include([
        path('', views.AnimalDetailsView.as_view(), name='details animal'),
        path('edit/', views.AnimalEditView.as_view(), name='edit animal'),
        path('delete/', views.AnimalDeleteView.as_view(), name='delete animal'),
    ])),


] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT))