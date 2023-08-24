from django.db import models
from django.contrib.auth.models import User

class Customers(models.Model):
    customer_name = models.CharField(max_length=25)
    customer_rank = models.CharField(max_length=20)
    customer_id = models.CharField(max_length=15, null=True, blank=True)
    customer_address = models.CharField(max_length=100, default='')
    customer_file = models.FileField(upload_to='media/', blank=True, null=True)

 

