from django.conf import settings
from django.db import models
from django.utils.text import slugify
# Create your models here.
class Product(models.Model):
    CATEGORY = [("Soups", "SOUPS"),
            ("Stews", "STEWS"),
            ("Proteins", "PROTEINS"),
            ("Side Dishes", "SIDE_DISHES"),
            ("Rice", "RICE"),
    ]
    name = models.CharField(max_length=100)
    slug = models.SlugField(blank=True, null=True)
    image = models.ImageField(upload_to="img")
    description = models.TextField(blank=True, null=True)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    category = models.CharField(max_length=100, choices=CATEGORY, blank=True, null=True)

    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        unique_slug = self.slug
        counter = 1
        if Product.objects.filter(slug=unique_slug).exists():
            unique_slug = f'{self.slug}-{counter}'
            counter += 1
        self.slug = unique_slug
        super().save(*args, **kwargs)

class Cart(models.Model):
    cart_code = models.CharField(max_length=11,unique=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, blank=True, null=True)
    paid = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, blank=True, null=True)

    def __str__(self):
        return self.cart_code

class CartItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='items')
    quantity = models.IntegerField(default=1)

    def __str__(self):
        return f"{self.quantity} x {self.product.name} in cart {self.cart.id}"
    
