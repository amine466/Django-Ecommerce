from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('login/', auth_views.LoginView.as_view(template_name="admin/login.html"), name="login"),
    path('logout/', auth_views.LogoutView.as_view(), name="logout"),

    path('', views.home, name='Dashboard'),
    path('settings', views.settings, name="Settings"),

    path('category', views.category, name='Category'),
    path('category/add', views.add_category, name='Add_Category'),
    path('category/edit/<int:pk>', views.edit_category, name='Edit_Category'),
    path('category/delete/<int:pk>', views.delete_category, name="Delete_Category"),

    path('product', views.product, name='Product'),
    path('product/add', views.add_product, name="Add_Product"),
    path('product/edit/<int:pk>', views.edit_product, name='Edit_Product'),
    path('product/delete/<int:pk>', views.delete_product, name="Delete_Category"),
    path('product/view/<int:pk>', views.view_product, name='View_Product'),

    path('customer', views.customer, name='Customer'),
    path('customer/add', views.add_customer, name='Add_Customer'),
    path('customer/edit/<int:pk>', views.edit_customer, name='Edit_Customer'),
    path('customer/delete/<int:pk>', views.delete_customer, name="Delete_Customer"),

    path('order', views.order, name="Order_List"),
    path('order/add', views.add_order, name='Add_Order'),
    path('order/edit/<int:pk>', views.edit_order, name="Edit_Order"),
    path('order/items/<int:pk>', views.order_items, name="Order_Items"),
    path('order/delete/<int:pk>', views.delete_order, name="Delete_Order"),
    path('order/view/<int:pk>', views.view_order, name="View_Order"),
]