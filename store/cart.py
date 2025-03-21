from admin_site.models import Product

class Cart():
    def __init__(self, request):
        self.session = request.session

        # Use 'cart' instead of 'session_key'
        cart = self.session.get('cart')

        # If no cart exists in the session, create an empty one
        if 'cart' not in self.session:
            cart = self.session['cart'] = {}

        self.cart = cart

    def add(self, product, quantity=1):
        product_id = str(product.id)
        if product_id not in self.cart:
            self.cart[product_id] = {
                'quantity': quantity,
                'price': str(product.price)
            }
        else:
            self.cart[product_id]['quantity'] += quantity
        self.save()

    def update(self, product_id, quantity):
        product_id = str(product_id)
        if product_id in self.cart:
            self.cart[product_id]['quantity'] = quantity
        self.save()

    def delete(self, product_id):
        product_id = str(product_id)
        if product_id in self.cart:
            del self.cart[product_id]
        self.save()

    def items(self):
        return [
            {
                'product': Product.objects.get(id=product_id),
                'quantity': item['quantity'],
                'price': float(item['price']),
                'total': float(item['price']) * item['quantity']
            }
            for product_id, item in self.cart.items()
        ]

    def get_total_price(self):
        return sum(float(item['price']) * int(item['quantity']) for item in self.cart.values())

    def __len__(self):
        return sum(item['quantity'] for item in self.cart.values())

    def save(self):
        self.session.modified = True

    def clear(self):
        if 'cart' in self.session:
            del self.session['cart']
        self.save()