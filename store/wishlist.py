from admin_site.models import Product

class Wishlist:
    def __init__(self, request):
        self.session = request.session
        wishlist = self.session.get('wishlist')

        if 'wishlist' not in self.session:
            wishlist = self.session['wishlist'] = {}

        self.wishlist = wishlist

    def add(self, product):
        product_id = str(product.id)
        if product_id not in self.wishlist:
            self.wishlist[product_id] = {'quantity': 1, 'price': str(product.price)}
        self.save()

    def delete(self, product_id):
        product_id = str(product_id)
        if product_id in self.wishlist:
            del self.wishlist[product_id]
        self.save()

    def items(self):
        return [
            {
                'product': Product.objects.get(id=key),
                'price': value['price']
            }
            for key, value in self.wishlist.items()
        ]
    
    def __len__(self):
        return len(self.wishlist)
    
    def save(self):
        self.session.modified = True