from itertools import count

from django.contrib.auth import get_user_model
from django.views import generic as views
from django.shortcuts import render, redirect, get_object_or_404
from django.conf import settings
from collections import defaultdict
from django.core.mail import EmailMessage
from django.template.loader import render_to_string

from farm_app.cart.cart import Cart
from farm_app.catalog.models import AnimalProduct, Nut, DairyProduct, VegetableAndFruit
from farm_app.order.models import Order, OrderItem

UserModel = get_user_model()

def start_order(request):
    cart = Cart(request)

    if request.method == "POST":
        user = request.user
        address = request.POST.get('address')
        city = request.POST.get('city')
        phone = request.POST.get('phone')

        order = Order.objects.create(user=user, first_name=user.first_name, last_name=user.last_name,
                                     email=user.email, address=address, city=city, phone=phone)
        seller_items = defaultdict(list)

        for item in cart:
            item_type = item['item_type']
            quantity = int(item['quantity'])

            if item_type == "VegetableAndFruit":
                fruit = item[item_type]
                dairy = None
                meat = None
                nut = None
                price = fruit.price * quantity

            elif item_type == "DairyProduct":
                dairy = item[item_type]
                fruit = None
                meat = None
                nut = None
                price = dairy.price * quantity

            elif item_type == "AnimalProduct":
                meat = item[item_type]
                dairy = None
                fruit = None
                nut = None
                price = meat.price * quantity

            else:
                nut = item[item_type]
                dairy = None
                meat = None
                fruit = None
                price = nut.price * quantity

            OrderItem.objects.create(order=order, fruit=fruit, meat=meat, dairy=dairy, nut=nut,
                                                  price=price,
                                                  quantity=quantity)

            if item['item_type'] == "VegetableAndFruit":
                seller_email = fruit.user.email
                seller_items[seller_email].append(f"Product: {fruit.name}, Quantity: {quantity}, Price: {price}")
            elif item['item_type'] == "DairyProduct":
                seller_email = dairy.user.email
                seller_items[seller_email].append(f"Product: {dairy.name}, Quantity: {quantity}, Price: {price}")
            elif item['item_type'] == "AnimalProduct":
                seller_email = meat.user.email
                seller_items[seller_email].append(f"Product: {meat.name}, Quantity: {quantity}, Price: {price}")
            else:
                seller_email = nut.user.email
                seller_items[seller_email].append(f"Product: {nut.name}, Quantity: {quantity}, Price: {price}")

        html_content = render_to_string('emails/order_confirmation.html', {'order': order, 'user': user})
        email = EmailMessage(
            'Order Confirmation - Farm Shop',
            html_content,
            settings.EMAIL_HOST_USER,
            [user.email],
        )
        email.content_subtype = 'html'
        email.send()

        for seller_email, items in seller_items.items():
            item_list = "\n".join(items)
            html_content = render_to_string('emails/seller_notification.html', {'items': item_list, 'order': order})
            seller_email_message = EmailMessage(
                'New Order Notification - Farm Shop',
                html_content,
                settings.EMAIL_HOST_USER,
                [seller_email],
            )
            seller_email_message.content_subtype = 'html'
            seller_email_message.send()

        cart.clear()

        return redirect('profile details', request.user.id)

    return redirect('cart')


class MyOrders(views.ListView):
    model = Order
    template_name = 'orders/my_orders.html'
    context_object_name = 'orders'

    def get_queryset(self):
        user = get_object_or_404(UserModel, pk=self.kwargs['pk'])
        return Order.objects.filter(user=user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        order_total_prices = {}

        for order in context['orders']:
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
        item_type = None
        product = None
        item_price = 0

        for product_type in ['meat', 'nut', 'dairy', 'fruit']:
            product_field = getattr(item, f'{product_type}_id', None)
            if product_field:
                item_type = product_type.capitalize()
                product_model = {
                    'Meat': AnimalProduct,
                    'Nut': Nut,
                    'Dairy': DairyProduct,
                    'Fruit': VegetableAndFruit
                }.get(item_type)
                product = get_object_or_404(product_model, pk=product_field)
                item_price = product.price
                break

        order_total += item_price * item.quantity
        items.append((item, item_type, product.id, item_price))

    context = {
        'items': items,
        'order': order,
        'order_items': len(order_items),
        'order_total': order_total,
    }

    return render(request, 'orders/order_details.html', context)
