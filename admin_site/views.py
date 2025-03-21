from django.shortcuts import render, redirect, get_object_or_404
from .models import Category, Product, Customer, Order, OrderItem, SiteSettings
from datetime import datetime
from .forms import CategoryForm, ProductForm, CustomerForm, OrderForm, SettingsForm
from django.core.paginator import Paginator
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy

# Create your views here.
@login_required
def home(request):
    now = datetime.now()
    current_year = now.year
    current_month = now.month
    current_day = now.day

    categories = Category.objects.count()
    products = Product.objects.count()
    today_orders = Order.objects.filter(
        created_at__year = current_year,
        created_at__month = current_month,
        created_at__day = current_day
    ).count()
    latest_orders = Order.objects.order_by('created_at')[:4]

    context = {
        'title': 'Dashboard',
        'categories': categories,
        'products': products,
        'orders': today_orders,
        'latest_orders': latest_orders,
    }
    return render(request, 'admin/index.html', context)

@login_required
def category(request):
    category_list = Category.objects.all()
    paginator = Paginator(category_list, 5)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {
        'title': 'Category',
        'page_obj': page_obj,
    }
    return render(request, 'admin/pages/category/category.html', context)

@login_required
def add_category(request):
    if request.method == "POST":
        add_form = CategoryForm(request.POST, request.FILES)
        if add_form.is_valid():
            new_category = add_form.save(commit=False)
            new_category.save()
            messages.success(request, 'Category Added Successfully')
            return redirect("Category")
    else:
        add_form = CategoryForm()
        context = {
            "form": add_form,
            'title': 'Create Category',
        }
    return render(request, "admin/pages/category/category_add.html", context)

@login_required
def edit_category(request, pk):
    category = get_object_or_404(Category, pk=pk)
    if request.method == "POST":
        edit_form = CategoryForm(request.POST, request.FILES, instance=category)
        if edit_form.is_valid():
            edit_form.save()
            messages.success(request, 'Category Updated Successfully')
            return redirect("Category")
    else:
        edit_form = CategoryForm(instance=category)
        context = {
            "form": edit_form,
            'title': 'Update Category'
        }
    return render(request, "admin/pages/category/category_edit.html", context)

@login_required
def delete_category(request, pk):
    category = get_object_or_404(Category, pk=pk)
    category.delete()
    messages.success(request, "Category Deleted Successfully")
    return redirect("Category")

@login_required
def product(request):
    product_list = Product.objects.all()
    paginator = Paginator(product_list, 5)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {
        'title': 'Product',
        'page_obj': page_obj,
    }
    return render(request, 'admin/pages/product/product.html', context)

@login_required
def add_product(request):
    if request.method == "POST":
        add_form = ProductForm(request.POST, request.FILES)
        if add_form.is_valid():
            new_product = add_form.save(commit=False)
            new_product.save()
            messages.success(request, 'Product Added Successfully')
            return redirect("Product")
    else:
        add_form = ProductForm()
        context = {
            "form": add_form,
            "title": "Create Product"
        }
    return render(request, "admin/pages/product/product_add.html", context)

@login_required
def edit_product(request, pk):
    product = get_object_or_404(Product, pk=pk)
    if request.method == "POST":
        edit_form = ProductForm(request.POST, request.FILES, instance=product)
        if edit_form.is_valid():
            edit_form.save()
            messages.success(request, 'Product Updated Successfully')
            return redirect("Product")
    else:
        edit_form = ProductForm(instance=product)
        context = {
            "form": edit_form,
            "title": "Update Product"
        }
    return render(request, "admin/pages/product/product_edit.html", context)

@login_required
def delete_product(request, pk):
    product = get_object_or_404(Product, pk=pk)
    product.delete()
    messages.success(request, "Product Deleted Successfully")
    return redirect("Product")

@login_required
def view_product(request, pk):
    product = get_object_or_404(Product, pk=pk)
    context = {
        'product': product,
        "title": "View Product",
    }
    return render(request, "admin/pages/product/product_view.html", context)

@login_required
def customer(request):
    customer_list = Customer.objects.all()
    paginator = Paginator(customer_list, 5)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {
        'title': 'Customer',
        'page_obj': page_obj,
    }
    return render(request, "admin/pages/customer/customer.html", context)

@login_required
def add_customer(request):
    if request.method == "POST":
        add_form = CustomerForm(request.POST)
        if add_form.is_valid():
            new_customer = add_form(commit=False)
            new_customer.save()
            messages.success(request, 'Customer Added Successfully')
            return redirect("Customer")
    else:
        add_form = CustomerForm()
        context = {
            "form": add_form,
            "title": "Create Customer"
        }
    return render(request, "admin/pages/customer/customer_add.html", context)

@login_required
def edit_customer(request, pk):
    customer = get_object_or_404(Customer, pk=pk)
    if request.method == "POST":
        edit_form = CustomerForm(request.POST, request.FILES, instance=customer)
        if edit_form.is_valid():
            edit_form.save()
            messages.success(request, 'Customer Updated Successfully')
            return redirect("Customer")
    else:
        edit_form = CustomerForm(instance=customer)
        context = {
            "form": edit_form,
            "title": "Update Customer"
        }
    return render(request, "admin/pages/customer/customer_edit.html", context)

@login_required
def delete_customer(request, pk):
    customer = get_object_or_404(Customer, pk=pk)
    customer.delete()
    messages.success(request, "Customer Deleted Successfully")
    return redirect("Customer")

@login_required
def order(request):
    order_list = Order.objects.all()
    paginator = Paginator(order_list, 5)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {
        'title': 'Order',
        'page_obj': page_obj,
    }
    return render(request, "admin/pages/order/order.html", context)

@login_required
def order_items(request, pk):
    order = get_object_or_404(Order, id=pk)
    products = Product.objects.filter(status='active')
    order_items = OrderItem.objects.filter(order=order)

    if request.method == "POST":
        OrderItem.objects.filter(order=order).delete()

        products_list = request.POST.getlist('products')
        quantities_list = request.POST.getlist('quantities')

        total_price = 0

        for product_id, quantity in zip(products_list, quantities_list):
            product = get_object_or_404(Product, id=product_id)
            quantity = int(quantity)
            OrderItem.objects.create(order=order, product=product, quantity=quantity, total=product.price * quantity)
            total_price += product.price * quantity

        order.total_price = total_price
        order.save()
        return redirect('Order_List')

    context = {
        'products': products,
        'order': order,
        'order_items': order_items,
        'title': 'Edit Order Items',
    }
    return render(request, 'admin/pages/order/order_item.html', context)

def add_order(request):
    if request.method == "POST":
        form = OrderForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            order.total_price = 0
            order.save()
            messages.success(request, 'Order Created Successfully')
            return redirect('Order_Items', pk=order.id)
    else:
        form = OrderForm()
        context = {
            'form': form,
            'title': 'Add Order',
        }
    return render(request, 'admin/pages/order/order_add.html', context)

def edit_order(request, pk):
    order = get_object_or_404(Order, pk=pk)
    if request.method == "POST":
        form = OrderForm(request.POST, instance=order)
        if form.is_valid():
            form.save()
            messages.success(request, 'Order Updated Successfully')
            return redirect('Order_Items', pk=order.id)
    else:
        form = OrderForm(instance=order)
        context = {
            'form': form,
            'title': 'Edit Order'
        }
        return render(request, "admin/pages/order/order_edit.html", context)
            
@login_required
def delete_order(request, pk):
    order = get_object_or_404(Order, pk=pk)
    order.delete()
    messages.success(request, "Order Deleted Successfully")
    return redirect("Order_List")

@login_required
def view_order(request, pk):
    order = get_object_or_404(Order, pk=pk)
    order_items = OrderItem.objects.filter(order=order)
    context = {
        'order': order,
        'order_items': order_items,
        'title': 'View Order'
    }
    return render(request, "admin/pages/order/order_view.html", context)

@login_required
def settings(request):
    site_settings, _ = SiteSettings.objects.get_or_create(pk=1)

    if request.method == 'POST':
        form = SettingsForm(request.POST, request.FILES, instance=site_settings)
        if form.is_valid():
            form.save()
            messages.success(request, "Settings updated successfully")
            return redirect(reverse_lazy('Settings'))
    else:
        form = SettingsForm(instance=site_settings)

    context = {
        'form': form,
        'title': 'Site Settings',
    }
    return render(request, 'admin/pages/settings.html', context)