from django.shortcuts import render, redirect, get_object_or_404
from admin_site.models import Category, Product, Customer, Order, OrderItem, SiteSettings
from .forms import SignupForm, LoginForm, CheckoutForm, ProfileForm, ChangePasswordForm
from django.contrib import messages
from .utils import unauthenticated_customer
from django.core.paginator import Paginator
from .cart import Cart
from .wishlist import Wishlist
from django.http import JsonResponse, Http404
from django.contrib.auth.hashers import make_password

# Create your views here.
def get_common_context(request, extra_context=None):
    settings = SiteSettings.objects.get(pk=1)

    customer_id = request.session.get("customer_id")
    if customer_id:
        customer = Customer.objects.get(id=customer_id)
    else:
        customer = None
    context = {
        'categories': Category.objects.filter(status='active'),
        'cart': Cart(request),
        'wishlist_count': len(Wishlist(request).items()), 
        'customer': customer,
        'settings': settings,
    }
    if extra_context:
        context.update(extra_context)
    return context

@unauthenticated_customer
def signup(request):
    if request.method == "POST":
        form = SignupForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Account created successfully")
            return redirect('Login')
    else:
        form = SignupForm()
    context = {
        'form': form,
        'title': 'Sign Up',
    }
    return render(request, "store/auth/signup.html", get_common_context(request, context))

@unauthenticated_customer
def login(request):
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data["email"]
            password = form.cleaned_data["password"]
            try:
                customer = Customer.objects.get(email=email)
                if customer.check_password(password):
                    request.session["customer_id"] = customer.id
                    return redirect('Index')
                else:
                    messages.error(request, "Invalid email or password")
            except Customer.DoesNotExist:
                messages.error(request, "Customer Not Found")
    else:
        form = LoginForm()
    context = {
        'form': form,
        'title': 'Login',
    }
    return render(request, "store/auth/login.html", get_common_context(request, context))

def profile(request):
    customer_id = request.session.get("customer_id")
    customer = Customer.objects.get(id=customer_id)

    if not customer_id:
        redirect('Login')

    if request.method == 'POST':
        form = ProfileForm(request.POST, instance=customer)
        if form.is_valid():
            form.save()
            messages.success(request, "Profile updated successfully!")
            return redirect('Profile')
    else:
        form = ProfileForm(instance=customer)
        context = {
            'form': form,
            'title': 'Profile',
        }
    return render(request, "store/profile/profile.html", get_common_context(request, context))

def change_password(request):
    customer_id = request.session.get("customer_id")
    if not customer_id:
        return redirect('Login')

    customer = Customer.objects.get(id=customer_id)

    if request.method == 'POST':
        form = ChangePasswordForm(request.POST, customer=customer)
        if form.is_valid():
            form.save()
            messages.success(request, "Password updated successfully!")
            return redirect('Profile')
    else:
        form = ChangePasswordForm(customer=customer)

    context = {
        'form': form,
        'title': 'Change Password',
    }
    return render(request, "store/profile/change_password.html", get_common_context(request, context))

def logout(request):
    del request.session["customer_id"]
    return redirect('Index')

def index(request):
    featured_products = Product.objects.filter(status='active', is_featured=True)
    featured_products = featured_products.order_by('?')[:8]
    context = {
        'featured_products': featured_products,
    }
    return render(request, "store/index.html", get_common_context(request, context))

def contact(request):
    context = {
        'title': "Contact Us",
    }
    return render(request, "store/contact.html", get_common_context(request, context))

def shop(request):
    products = Product.objects.filter(status='active')

    category_id = request.GET.get('category')
    if category_id and category_id != 'all':  
        products = products.filter(category_id=category_id)

    min_price = Product.objects.order_by('price').first().price if Product.objects.exists() else 0
    max_price = Product.objects.order_by('-price').first().price if Product.objects.exists() else 0

    min_price_filter = request.GET.get('min_price', min_price)
    max_price_filter = request.GET.get('max_price', max_price)

    products = products.filter(price__gte=min_price_filter, price__lte=max_price_filter)

    sort_option = request.GET.get('sort')
    if sort_option == 'price-asc':
        products = products.order_by('price')
    elif sort_option == 'price-desc':
        products = products.order_by('-price')

    paginator = Paginator(products, 9)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'page_obj': page_obj,
        'product_count': paginator.count,
        'min_price': min_price,
        'max_price': max_price,
        'selected_min_price': min_price_filter,
        'selected_max_price': max_price_filter,
        'title': "Shop",
    }
    return render(request, "store/shop/shop.html", get_common_context(request, context))

def product(request, slug):
    product = get_object_or_404(Product, slug=slug)
    related_products = Product.objects.filter(status="active", category=product.category).exclude(id=product.id)
    related_products = related_products.order_by('?')[:4]
    category = product.category
    context = {
        'product': product,
        'cat': category,
        'related_products': related_products,
        'title': product.name,
    }
    return render(request, "store/shop/product.html", get_common_context(request, context))

def cart(request):
    cart = Cart(request)
    cart_items = cart.items()
    for item in cart_items:
        item['total'] = float(item['price']) * item['quantity']
    cart_subtotal = sum((item['price']) * item['quantity'] for item in cart_items)
    cart_total = cart_subtotal
    context = {
        'cart_items': cart_items,
        'cart_subtotal': cart_subtotal,
        'cart_total': cart_total,
        'title': 'Cart',
    }
    return render(request, "store/shop/shopping-cart.html", get_common_context(request, context))

def cart_add(request, id):
    product = get_object_or_404(Product, id=id)
    cart = Cart(request)
    cart.add(product=product)
    return redirect('Cart')

def cart_update(request, id):
    cart = Cart(request)
    quantity = request.GET.get('quantity')

    if quantity and quantity.isdigit():
        quantity = int(quantity)
        if quantity > 0:
            cart.cart[str(id)]['quantity'] = quantity
        else:
            cart.delete(id)
    cart.save()
    return redirect('Cart')

def cart_delete(request, id):
    cart = Cart(request)
    cart.delete(id)
    return redirect('Cart')

def wishlist(request):
    wishlist = Wishlist(request)
    wishlist_items = wishlist.items()

    context = {
        'wishlist_items': wishlist_items,
        'title': 'Wishlist',
    }
    return render(request, "store/shop/wishlist.html", get_common_context(request, context))

def add_wishlist(request, id):
    try:
        product = get_object_or_404(Product, id=id)
        wishlist = Wishlist(request)
        wishlist.add(product=product)
        wishlist_count = len(wishlist.items())
        return JsonResponse({'wishlist_count': wishlist_count})
    except Exception as e:
        print(f"Error adding to wishlist: {e}")
        return JsonResponse({'error': 'An error occurred while adding to the wishlist.'}, status=500)

def delete_wishlist(request, id):
    wishlist = Wishlist(request)
    wishlist.delete(id)
    return redirect('Wishlist')

def move_to_cart(request, id):
    product = get_object_or_404(Product, id=id)
    
    cart = Cart(request)
    cart.add(product)

    wishlist = Wishlist(request)
    wishlist.delete(id)
    return redirect('Wishlist')

def search(request):
    query = request.POST.get('query', '')

    products = Product.objects.filter(name__icontains=query) if query else Product.objects.all()

    min_price = Product.objects.order_by('price').first().price if Product.objects.exists() else 0
    max_price = Product.objects.order_by('-price').first().price if Product.objects.exists() else 0

    min_price_filter = float(request.GET.get('min_price', min_price))
    max_price_filter = float(request.GET.get('max_price', max_price))

    products = products.filter(price__gte=min_price_filter, price__lte=max_price_filter)

    paginator = Paginator(products, 9)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'title': "Search",
        'page_obj': page_obj,
        'product_count': paginator.count,
        'min_price': min_price,
        'max_price': max_price,
        'selected_min_price': min_price_filter,
        'selected_max_price': max_price_filter,
        'query': query,
    }
    return render(request, "store/shop/search.html", get_common_context(request, context))

def create_order_from_cart(customer, cart, address, city, country, postcode):
    order = Order.objects.create(
        customer=customer,
        address=address,
        city=city,
        country=country,
        postcode=postcode,
        total_price=cart.get_total_price())

    for item in cart.items():
        OrderItem.objects.create(
            order = order,
            product = item['product'],
            quantity = item['quantity'],
            total = item['price'] * item['quantity']
        )
    
    cart.clear()
    return order

def checkout(request):
    customer_id = request.session.get("customer_id")
    cart = Cart(request)
    cart_items = cart.items()
    cart_subtotal = cart.get_total_price()
    cart_total = cart_subtotal
    
    if not customer_id:
        return redirect('Login')

    customer = Customer.objects.get(id=customer_id)

    if request.method == 'POST':
        form = CheckoutForm(request.POST)
        if form.is_valid():
            create_order_from_cart(
                customer,
                cart,
                address=form.cleaned_data['address'],
                city=form.cleaned_data['city'],
                country=form.cleaned_data['country_state'],
                postcode=form.cleaned_data['postcode'],
                )
            return redirect('Orders')
    else:
        form = CheckoutForm()

    context = {
        'form': form,
        'customer': customer,
        'cart_items': cart_items,
        'cart_subtotal': cart_subtotal,
        'cart_total': cart_total,
        'title': 'Checkout',
    }
    return render(request, "store/shop/checkout.html", get_common_context(request, context))

def orders(request):
    customer_id = request.session.get("customer_id")
    customer = get_object_or_404(Customer, id=customer_id)
    orders = Order.objects.filter(customer=customer)

    if not customer_id:
        return redirect('Login') 
    
    context = {
        'orders': orders,
        'title': 'Orders',
    }
    return render(request, "store/profile/orders.html", get_common_context(request, context))

def order(request, id):
    order = get_object_or_404(Order, id=id)
    customer_id = request.session.get("customer_id")

    if not customer_id:
        return redirect('Login')
    
    if order.customer.id != customer_id:
        raise Http404("Order not found")
    
    context = {
        'order': order,
        'title': "Order Details",
    }
    return render(request, "store/profile/order.html", get_common_context(request, context))