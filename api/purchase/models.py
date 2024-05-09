from django.db import models
import uuid

# Create your models here.
class PurchaseOrder(models.Model):
    STATUS_CHOICES = [
        ('pending', 'pending'),
        ('completed', 'completed'),
        ('cancelled', 'cancelled'),
    ]

    po_number = models.CharField(primary_key = True, default = uuid.uuid4(),editable = False)
    vendor = models.ForeignKey("vendor.Vendor", on_delete=models.CASCADE , blank=True , null = True)
    order_date = models.DateTimeField()
    delivery_date = models.DateTimeField(null=True, blank=True)
    items = models.JSONField()
    quantity = models.IntegerField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    quality_rating = models.FloatField(null=True, blank=True)
    issue_date = models.DateTimeField(null=True,blank=True)
    acknowledgment_date = models.DateTimeField(null=True, blank=True)
    
    def __str__(self):
        return self.po_number