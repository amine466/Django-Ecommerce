from django import forms
from .models import Category, Product, Customer, Order, SiteSettings
from django.contrib.auth.hashers import make_password

class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name', 'status', 'image']

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'category', 'color', 'image', 'price', 'description', 'status', 'is_featured']

class CustomerForm(forms.ModelForm):
    confirm_password = forms.CharField(widget=forms.PasswordInput())
    class Meta:
        model = Customer
        fields = ['first_name', 'last_name', 'email', 'phone', 'password']
        widgets = {
            'password': forms.PasswordInput(),
        }

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")

        if password and confirm_password and password != confirm_password:
            self.add_error('confirm_password', "Passwords do not match")

        if password:
            cleaned_data["password"] = make_password(password)

        return cleaned_data
    
class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['customer', 'address', 'city', 'country', 'postcode', 'status']

class SettingsForm(forms.ModelForm):
    class Meta:
        model = SiteSettings
        fields = ['name', 'icon', 'logo', 'banner', 'hero', 'address', 'phone', 'email', 'facebook', 'twitter', 'linkedin', 'pintrest']