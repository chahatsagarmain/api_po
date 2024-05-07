from rest_framework.serializers import ModelSerializer
from .models import PurchaseOrder
from vendor.serializers import VendorSerializer
from vendor.models import Vendor

class PurchaseSerializer(ModelSerializer):
    vendor = VendorSerializer(source="vendor_set",many=True, read_only=True)  
    class Meta:
        model = PurchaseOrder
        fields = '__all__'
        
