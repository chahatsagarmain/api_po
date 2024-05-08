from django.db import models
from django.utils import timezone

class Vendor(models.Model):
    name = models.CharField(max_length=100, unique=True, blank=False)
    contact_details = models.TextField(blank=False)
    address = models.TextField(blank=False)
    vendor_code = models.CharField(max_length=50, unique=True, blank=False)
    on_time_delivery_rate = models.FloatField(default=0.0)
    quality_rating_avg = models.FloatField(default=0.0)
    average_response_time = models.FloatField(default=0.0)
    fulfillment_rate = models.FloatField(default=0.0)
    num_orders = models.IntegerField(default=0)
    
    def __str__(self):
        return self.name

class HistoricalPerformance(models.Model):
    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE)
    date = models.DateTimeField()
    on_time_delivery_rate = models.FloatField(default=0.0)
    quality_rating_avg = models.FloatField(default=0.0)
    average_response_time = models.FloatField(default=0.0)
    fulfillment_rate = models.FloatField(default=0.0)

    def __str__(self):
        return f"{self.vendor} - {self.date}"
