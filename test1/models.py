from django.db import models

# Create your models here.
class Product(models.Model):
    product_id = models.CharField(max_length=30, unique=True)
    product_name = models.CharField(max_length=30)
    product_description = models.CharField(max_length=400)
    product_category = models.CharField(max_length=100)
    product_img = models.ImageField(upload_to='images/')
    
    def __str__(self):
        return self.product_id

# Sir ka naya Contact Form table model
class Contact_Query(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    message = models.TextField()

    def __str__(self):
        return self.name