from django.db import models

# Create your models here.
class Client(models.Model):
    full_name = models.CharField(max_length=100)
    email = models.EmailField(max_length=100)
    phone = models.CharField(max_length=15)
    address = models.CharField(max_length=250)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    zip_code = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return(f"{self.full_name}  {self.email} {self.created_at} ") 
    
    # Model for Product
class Product(models.Model):
    client = models.ForeignKey(Client, on_delete=models.CASCADE, related_name='product')
    product_name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Product for {self.client.full_name} price {self.price}"