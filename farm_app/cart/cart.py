from itertools import count

from _decimal import Decimal
from django.apps import apps
from django.conf import settings
from django.core import serializers
from django.shortcuts import render


class Cart(object):
    def __init__(self, request):
        self.session = request.session
        cart = self.session.get(settings.CART_SESSION_ID)

        if not cart:
            cart = self.session[settings.CART_SESSION_ID] = {}

        self.cart = cart

    def __iter__(self):
        for prod in self.cart.keys():
            product_model = apps.get_model(app_label='catalog', model_name=self.cart[str(prod)]['item_type'])
            self.cart[str(prod)][self.cart[str(prod)]['item_type']] = product_model.objects.get(pk=prod)
            self.cart[str(prod)]['product'] = product_model.objects.get(pk=prod)

        for item in self.cart.values():
            product_model = item['item_type']
            item['total_price'] = Decimal(item[product_model].price * item['quantity'])
            yield item

    def __len__(self):
        return self.cart.values().__len__()

    def save(self):
        self.session[settings.CART_SESSION_ID] = self.cart
        self.session.modified = True

    def add(self, product_id, item_type, quantity,update_quantity=False):
        product_id = str(product_id)
        product_model = apps.get_model(app_label='catalog',model_name=item_type)

        if product_id not in self.cart:
            self.cart[product_id] = {'quantity': 1, 'id': product_id,'item_type':item_type, item_type:None}

        if update_quantity:
            self.cart[product_id]['quantity'] += int(quantity)

            if self.cart[product_id]['quantity'] == 0:
                self.remove(product_id)

        self.cart[product_id][item_type] = product_model.objects.get(pk=product_id)
        self.save()

    def remove(self,product_id):
        if str(product_id) in self.cart:
            del self.cart[str(product_id)]
            self.save()

    def clear(self):
        del self.session[settings.CART_SESSION_ID]
        self.session.modified = True


    def get_total_cost(self):
        total_cost = 0
        for item in self.cart.values():
            item_type = item['item_type']
            product_model = apps.get_model(app_label='catalog', model_name=item_type)
            product = product_model.objects.get(pk=item['id'])
            total_cost += product.price * item['quantity']
        return total_cost

    def get_item(self, product_id):
        if str(product_id) in self.cart:
            return self.cart[str(product_id)]
        else:
            return None
