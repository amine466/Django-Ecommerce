from django.db import models
from django.utils.text import slugify
from django.contrib.auth.hashers import check_password

# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length=50)
    slug = models.SlugField(unique=True)
    image = models.ImageField(upload_to='categories/')
    STATUS = (
        ('active', 'Active'),
        ('not_active', 'Not Active'),
    )
    status = models.CharField(max_length=10, choices=STATUS, default='Active')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name
    
class Customer(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    phone = models.CharField(max_length=20, unique=True)
    email = models.EmailField(max_length=50, unique=True)
    password = models.CharField(max_length=100)

    def check_password(self, raw_password):
        return check_password(raw_password, self.password)
    
    def __str__(self):
        return self.first_name + ' ' + self.last_name

class Product(models.Model):
    name = models.CharField(max_length=50)
    slug = models.SlugField(unique=True, blank=True)
    color = models.CharField(max_length=20)
    STATUS = (
        ('active', 'Active'),
        ('not_active', 'Not Active'),
    )
    status = models.CharField(max_length=10, choices=STATUS, default='active')
    price = models.DecimalField(default=0, decimal_places=2, max_digits=10)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    description = models.TextField()
    image = models.ImageField(upload_to='products/')
    is_featured = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.name)
            color_slug = slugify(self.color)
            self.slug = f"{base_slug}-{color_slug}"
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name
    
class Order(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    address = models.CharField(max_length=150)
    city = models.CharField(max_length=50)
    country = models.CharField(max_length=100)
    postcode = models.CharField(max_length=20)
    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('shipped', 'Shipped'),
        ('delivered', 'Delivered'),
        ('cancelled', 'Cancelled'),
    )
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveBigIntegerField()
    total = models.DecimalField(max_digits=10, decimal_places=2)
    
    def __str__(self):
        return f"{self.quantity} x {self.product.name}"
    
class SiteSettings(models.Model):
        name = models.CharField(max_length=30, verbose_name="Website Name")
        icon = models.ImageField(upload_to="settings/", null=True,  verbose_name="Website Icon")
        logo = models.ImageField(upload_to="settings/",  verbose_name="Website Logo")
        banner = models.ImageField(upload_to="settings/", verbose_name="Website Banner")
        hero = models.ImageField(upload_to="settings/", verbose_name="Website Hero")
        address = models.CharField(max_length=100, verbose_name="Address")
        phone = models.CharField(max_length=20, verbose_name="Phone")
        email = models.EmailField(max_length=30)
        facebook = models.CharField(max_length=50)
        twitter = models.CharField(max_length=50)
        linkedin = models.CharField(max_length=50)
        pintrest = models.CharField(max_length=50)