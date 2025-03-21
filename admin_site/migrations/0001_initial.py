# Generated by Django 5.1.7 on 2025-03-21 21:15

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('slug', models.SlugField(unique=True)),
                ('image', models.ImageField(upload_to='categories/')),
                ('status', models.CharField(choices=[('active', 'Active'), ('not_active', 'Not Active')], default='Active', max_length=10)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='Customer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=50)),
                ('last_name', models.CharField(max_length=50)),
                ('phone', models.CharField(max_length=20, unique=True)),
                ('email', models.EmailField(max_length=50, unique=True)),
                ('password', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='SiteSettings',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=30, verbose_name='Website Name')),
                ('icon', models.ImageField(null=True, upload_to='settings/', verbose_name='Website Icon')),
                ('logo', models.ImageField(upload_to='settings/', verbose_name='Website Logo')),
                ('banner', models.ImageField(upload_to='settings/', verbose_name='Website Banner')),
                ('hero', models.ImageField(upload_to='settings/', verbose_name='Website Hero')),
                ('address', models.CharField(max_length=100, verbose_name='Address')),
                ('phone', models.CharField(max_length=20, verbose_name='Phone')),
                ('email', models.EmailField(max_length=30)),
                ('facebook', models.CharField(max_length=50)),
                ('twitter', models.CharField(max_length=50)),
                ('linkedin', models.CharField(max_length=50)),
                ('pintrest', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('address', models.CharField(max_length=150)),
                ('city', models.CharField(max_length=50)),
                ('country', models.CharField(max_length=100)),
                ('postcode', models.CharField(max_length=20)),
                ('status', models.CharField(choices=[('pending', 'Pending'), ('shipped', 'Shipped'), ('delivered', 'Delivered'), ('cancelled', 'Cancelled')], default='pending', max_length=20)),
                ('total_price', models.DecimalField(decimal_places=2, max_digits=10)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('customer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='admin_site.customer')),
            ],
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('slug', models.SlugField(blank=True, unique=True)),
                ('color', models.CharField(max_length=20)),
                ('status', models.CharField(choices=[('active', 'Active'), ('not_active', 'Not Active')], default='active', max_length=10)),
                ('price', models.DecimalField(decimal_places=2, default=0, max_digits=10)),
                ('description', models.TextField()),
                ('image', models.ImageField(upload_to='products/')),
                ('is_featured', models.BooleanField(default=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='admin_site.category')),
            ],
        ),
        migrations.CreateModel(
            name='OrderItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.PositiveBigIntegerField()),
                ('total', models.DecimalField(decimal_places=2, max_digits=10)),
                ('order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='items', to='admin_site.order')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='admin_site.product')),
            ],
        ),
    ]
