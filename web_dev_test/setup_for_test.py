import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ecommerce.settings')
django.setup()

from django.contrib.auth.models import User
from store.models import Product, Customer

# Create a user
user, created = User.objects.get_or_create(username='testuser')
if created:
    user.set_password('testpassword')
    user.save()

# Create a customer for the user
Customer.objects.get_or_create(user=user, name=user.username, email=user.email)

# Create a product
Product.objects.get_or_create(name='Test Product', price=10.00)
