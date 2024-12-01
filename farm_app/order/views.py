from itertools import count

from django.contrib.auth import get_user_model
from django.views import generic as views
from django.shortcuts import render, redirect, get_object_or_404

from farm_app.cart.cart import Cart
from farm_app.catalog.models import AnimalProduct, Nut, DairyProduct, VegetableAndFruit
from farm_app.order.models import Order, OrderItem

UserModel = get_user_model()

def start_order(request):
    cart = Cart(request)

    if request.method == "POST":
        user = request.user
        first_name = user.first_name
        last_name = user.last_name
        email = user.email
        address = request.POST.get('address')
        zipcode = request.POST.get('zipcode')
        city = request.POST.get('city')
        phone = request.POST.get('phone')

        order = Order.objects.create(user=user, first_name=first_name, last_name=last_name,
                                     email=email, address=address, zipcode=zipcode, city=city, phone=phone)

        for item in cart:
            quantity = int(item['quantity'])

            if item['item_type'] == "VegetableAndFruit":
                fruit = item[item['item_type']]
                dairy = None
                meat = None
                nut = None
                price = fruit.price * quantity

            elif item['item_type'] == "DairyProduct":
                dairy = item[item['item_type']]
                fruit = None
                meat = None
                nut = None
                price = dairy.price * quantity

            elif item['item_type'] == "AnimalProduct":
                meat = item[item['item_type']]
                dairy = None
                fruit = None
                nut = None
                price = meat.price * quantity

            else:
                nut = item[item['item_type']]
                dairy = None
                meat = None
                fruit = None
                price = nut.price * quantity

            item = OrderItem.objects.create(order=order, fruit=fruit, meat=meat, dairy=dairy, nut=nut, price=price,
                                            quantity=quantity)

        cart.clear()

        return redirect('profile details', request.user.id)

    return redirect('cart')


class MyOrders(views.ListView):
    model = Order
    template_name = 'orders/my_orders.html'
    context_object_name = 'order'

    def model_name(self, product):
        return str(product.__class__.__name__)

    def get_queryset(self):
        user = get_object_or_404(UserModel, pk=self.kwargs['pk'])
        return Order.objects.filter(user=user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        order_total_prices = {}

        for order in context['order']:
            total_price = sum(item.price for item in order.items.all())
            order_total_prices[order.id] = total_price
            order.update_status()


        context={
            'order_total_prices' :order_total_prices,
            'count_of_my_orders': len(order_total_prices)
        }

        return context

def order_details(request, pk):
    order = get_object_or_404(Order, pk=pk)
    order_items = order.items.all()
    order_total = 0
    items = []

    for item in order_items :
        if item.meat_id is not None:
            item_id = item.meat_id
            item_type = 'AnimalProduct'
            product = get_object_or_404(AnimalProduct, pk=item_id)
            item_price = float(product.price)

        elif item.nut_id is not None:
            item_id = item.nut_id
            item_type ='Nut'
            product = get_object_or_404(Nut, pk=item_id)
            item_price = float(product.price)

        elif item.dairy_id is not None:
            item_id = item.dairy_id
            item_type = 'DairyProduct'
            product = get_object_or_404(DairyProduct, pk=item_id)
            item_price = float(product.price)

        else:
            item_id = item.fruit_id
            item_type = 'VegetableAndFruit'
            product = get_object_or_404(VegetableAndFruit, pk=item_id)
            item_price = float(product.price)

        order_total += item.price
        items.append((item, item_type, item_id, item_price))

    context = {
        'items' : items,
        'order': order,
        'order_items': order_items.count(),
        'order_total': order_total,
    }

    return render(request, 'orders/order_details.html', context)
