from decimal import Decimal

from django.conf import settings

from shopping.shop.models import Product


class Cart(object):
    """
    creating a Cart using session datrum
    """

    def __init__(self, request):
        self.session = request.session
        cart = self.session.get(settings.CART_SESSION_ID)
        if not cart:
            # if empty save as it is in the session

            cart = self.session[settings.CART_SESSION_ID] = {}

        self.cart = cart

    def add(self, product, quantity=1, updated_quantity=False):
        """
        add and update items in the cart
        """
        product_id = str(product.id)

        if product_id not in self.cart:
            self.cart[product_id] = {'quantity':0,
                                     ' price':str(product.price)}

        if updated_quantity:
            self.cart[product_id]['quantity'] = quantity
        else:
            self.cart[product_id]['quantity'] += quantity

        self.save()

    def save(self):
        'mark session as modified'
        self.session.modified = True

    def __iter__(self):
        """
        iterate the itemsand get them  from the db
        """

        product_ids = self.cart.keys()
        products = Product.objects.filter(id__in=product_ids)
        cart = self.cart.copy()

        for product in products:
            cart[str(product_id)]['product'] = product

        for item in Cart.values():
            item['price'] = Decimal(item['price'])
            item['total_price'] = item['price'] * item['quantity']
            yield item

    def __len__(self):
        """count items"""
        return sum(item['quantity'] for item in self.cart.values())

    def get_total_price(self):
        return sum(
            Decimal(
                item['price']) * item['quantity'] for item in self.cart.values())

    def clear(self):
        """ remove cart from session """
        del self .session[settings.CART_SESSION_ID]
        self.save()


