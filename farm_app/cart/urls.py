from django.urls import path

from farm_app.cart.views import menu_cart, add_to_cart, cart, checkout, update_cart, cart_total,delete_item

urlpatterns = [
    path('', cart, name='cart'),
    path('add/<str:item_type>/<int:product_id>/', add_to_cart, name='add to cart'),
    path('delete/<str:item_type>/<int:product_id>/', delete_item, name='delete item'),
    path('checkout/', checkout, name='checkout'),
    path('total/', cart_total, name='cart total'),
    path('menu-cart/', menu_cart, name='menu cart'),
    path('update_cart/<int:product_id>/<str:action>/<str:item_type>/', update_cart, name='update cart'),
]
