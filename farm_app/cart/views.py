from django.apps import apps
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404
from django.template.loader import render_to_string
from django.urls import reverse

from farm_app.cart.cart import Cart
from json import JSONEncoder


def _default(self, obj):
    return getattr(obj.__class__, "to_json", _default.default)(obj)


_default.default = JSONEncoder().default
JSONEncoder.default = _default


@login_required(login_url='/login/')
def add_to_cart(request, item_type, product_id):
    current_cart = Cart(request)
    model = apps.get_model('catalog', item_type)
    product = get_object_or_404(model, pk=product_id)

    cart_item = current_cart.get_item(product_id)
    if cart_item:
        current_cart.add(product_id, item_type, quantity=1, update_quantity=True)
    else:
        current_cart.add(product_id, item_type, quantity=0, update_quantity=True)

    current_cart.save()

    product.is_in_the_cart = True
    product.save()

    response_data = {
        'success': True,
        'cart_html': render_to_string('cart/menu_cart.html', {'cart': current_cart}),
        'redirect_url': reverse('cart'),
    }

    return JsonResponse(response_data)


def cart(request):
    current_cart = Cart(request)

    context = {
        'total_items': len(current_cart)
    }

    return render(request, 'cart/cart.html', context=context)


def update_cart(request, product_id, action, item_type):
    current_cart = Cart(request)
    if action == 'increment':
        current_cart.add(product_id, item_type, 1, True)
    else:

        current_cart.add(product_id, item_type, quantity=-1, update_quantity=True)

    product_model = apps.get_model(app_label='catalog', model_name=item_type)
    product = product_model.objects.get(pk=product_id)
    quantity = current_cart.get_item(product_id)

    if quantity:
        quantity = quantity['quantity']

        item = {
            'product': {
                'id': product.id,
                'name': str(product),
                'photo': product.photo,
                'price': product.price,
            },
            'total_price': (quantity * product.price),
            'quantity': quantity,
            'item_type': item_type,
        }
    else:
        item = None

    context = {
        'item': item,
        'total_cart_price': current_cart.get_total_cost,
        'success': True,
        'cart_html': render_to_string('cart/menu_cart.html', {'cart': cart}),
        'redirect_url': reverse('cart'),
    }
    response = render(request, 'cart/cart_item.html', context)
    response['HX-Trigger'] = 'update-menu-cart'

    return response


@login_required(login_url='/login/')
def delete_item(request, item_type, product_id):
    current_cart = Cart(request)
    current_cart.remove(product_id)


    response_data = {
        'success': True,
        'cart_html': render_to_string('cart/menu_cart.html', {'cart': current_cart}),
        'cart_length': len(current_cart),
    }
    return JsonResponse(response_data)


@login_required
def checkout(request):
    return render(request, 'cart/checkout.html')


def menu_cart(request):
    return render(request, 'cart/menu_cart.html')


def cart_total(request):
    return render(request, 'cart/cart_total.html')
