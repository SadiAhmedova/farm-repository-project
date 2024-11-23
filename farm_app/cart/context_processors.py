from farm_app.farm_app.cart.cart import Cart


def cart(request):
    return {'cart': Cart(request)}