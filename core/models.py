from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from cloudinary_storage.storage import MediaCloudinaryStorage

class Product(models.Model):
    CATEGORY_CHOICES = [
        ('living', 'Living Room'),
        ('bedroom', 'Bedroom'),
        ('dining', 'Dining & Kitchen'),
    ]

    name = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    # Use default storage (Cloudinary) explicitly
    image = models.ImageField(
        upload_to='product_images/',
        blank=True,
        null=True,
        storage=MediaCloudinaryStorage()
    )
    rating = models.PositiveIntegerField(default=0)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
    


class ContactMessage(models.Model):
    name = models.CharField(max_length=100)
    phone = models.CharField(max_length=15, blank=True, null=True)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} - {self.created_at.strftime('%Y-%m-%d %H:%M')}"



class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'product')   # prevent duplicate items

    def __str__(self):
        return f"{self.product.name} ({self.quantity})"

    def total_price(self):
        return self.quantity * self.product.price



class Payment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    location = models.CharField(max_length=255)
    delivery_date = models.DateField()
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    advance_payment = models.DecimalField(max_digits=10, decimal_places=2)
    remaining_amount = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"Payment for {self.product.name} by {self.user.username}"