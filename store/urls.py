from django.urls import path
from . import views

urlpatterns = [
    path('register', views.signup, name="Signup"),
    path('login', views.login, name="Login"),
    path('profile', views.profile, name="Profile"),
    path('change-password', views.change_password, name="Change_Password"),
    path('logout', views.logout, name="Logout"),

    path('', views.index, name="Index"),
    path('shop', views.shop, name="Shop"),
    path('shop/<slug:slug>/', views.product, name="Product"),
    path('search', views.search, name="Search"),

    path('cart', views.cart, name="Cart"),
    path('cart/add/<int:id>/', views.cart_add, name="Add_Cart"),
    path('cart/edit/<int:id>/', views.cart_update, name="Update_Cart"),
    path('cart/delete/<int:id>/', views.cart_delete, name="Delete_Cart"),

    path('wishlist',views.wishlist, name="Wishlist"),
    path('wishlist/add/<int:id>/', views.add_wishlist, name="Add_Wishlist"),
    path('wishlist/delete/<int:id>/', views.delete_wishlist, name="Delete_Wishlist"),
    path('wishlist/move/<int:id>/', views.move_to_cart, name="Move_Cart"),

    path('checkout', views.checkout, name="Checkout"),
    path('orders', views.orders, name="Orders"),
    path('order/<int:id>/', views.order, name="Order"),

    path('contact', views.contact, name="Contact"),
]