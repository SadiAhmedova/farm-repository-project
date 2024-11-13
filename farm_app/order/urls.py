from django.urls import path

from farm_app.order.views import start_order, MyOrders,order_details

urlpatterns = [
    path('start_order/', start_order, name='start order'),
    path('my_orders/<int:pk>/', MyOrders.as_view(), name='my orders'),
    path('order_details/<int:pk>/', order_details, name="detail order"),
]