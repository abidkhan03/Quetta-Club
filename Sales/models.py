from email.policy import default
from enum import auto
from unicodedata import name
from django.db import models
from Customers.models import Customers
from django.utils import timezone

class Sales(models.Model):

    bill_no = models.CharField(max_length=20)
    PoS_no = models.CharField(max_length=50, null=True, blank=True)
    month = models.CharField(max_length=50, null=True, blank=True)
    created_date = models.DateField()
    created_on  = models.DateTimeField(auto_now_add=True)
    address = models.CharField(max_length=50, null=False, blank=False)
    account_of = models.CharField(max_length=50, null=False, blank=False)
    amount = models.PositiveIntegerField()
    discount = models.PositiveIntegerField(null=True, blank=True)
    net_amount = models.PositiveIntegerField()
    remarks = models.CharField(max_length=50, null=True, blank=True)    
    customer_id = models.ForeignKey(Customers, on_delete=models.CASCADE, null=True, blank=True)

    def publish_date(self):
        return self.created_date.strftime('%d-%m-%Y')



class Bill(models.Model):
    STATUS = (
        ('paid', 'Paid'),
        ('complementery', 'Complementery'),
        ('cancelled', 'Cancelled')
    )
    status = models.CharField(max_length=50, choices=STATUS, null=True, blank=True)
    rv_no = models.CharField(max_length=50, null=True) # only paid modal will have this field
    date = models.DateField() # all modal will have this field
    amount = models.PositiveIntegerField(default=0) # paid and complete modal will have this field
    bill_remarks = models.CharField(max_length=50, null=True, blank=True) # only complete modal will have this field
    reason = models.CharField(max_length=50, null=True, blank=True) # only cancel modal will have this field
    sale_id = models.ForeignKey(Sales, on_delete=models.CASCADE)


class dummyTable(models.Model):
    bill_no = models.PositiveIntegerField()
    rank= models.CharField(max_length=50, null=True, blank=True)
    pos_no= models.CharField(max_length=50, null=True, blank=True)
    cname = models.CharField(max_length=50, null=True, blank=True)
    address = models.CharField(max_length=50,  null=True, blank=True)
    account_of = models.CharField(max_length=50, null=True, blank=True)
    date= models.DateField(default=timezone.now)
    month= models.CharField(max_length=50, null=True, blank=True)
    amount= models.CharField(max_length=50, null=True, blank=True)
    discount= models.CharField(max_length=50, null=True, blank=True)
    net_amount= models.CharField(max_length=50, null=True, blank=True)
    remarks= models.CharField(max_length=50, null=True, blank=True)
    status= models.CharField(max_length=50, default='exist', null=True, blank=True)
