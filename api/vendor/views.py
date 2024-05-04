from rest_framework.views import APIView
from .models import Vendor
from .serializers import VendorSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status

class VendorView(APIView):
    permission_classes = [IsAuthenticated,]
    
    def get(self, request , format=None):
        query_set = Vendor.objects.all()
        serialized_data = VendorSerializer(query_set , many = True)
        return Response({"data" : serialized_data.data})
    
    def post(self , request , format=None):
        try:
            serialized_vendor = VendorSerializer(data=request.data)
            serialized_vendor.is_valid(raise_exception=True)
            serialized_vendor.save()  # Use save() instead of create()
            
            return Response(data={"message": "Vendor created", "data": serialized_vendor.data}, status=status.HTTP_200_OK)
        
        except Exception as e:
            return Response(data={"message": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class VendorViewById(APIView):
    permission_classes = [IsAuthenticated,]
    
    def get(self, request, pk, format=None):        
        try:
            vendor = Vendor.objects.get(id=pk)
            serialized_data = VendorSerializer(vendor)
            return Response(data={"data": serialized_data.data})
        except Vendor.DoesNotExist:
            return Response(data={"message": "User not found with ID"}, status=status.HTTP_404_NOT_FOUND)

    def put(self, request , pk , format=None):
        
        try:
            updated = Vendor.objects.filter(id=pk).update(**request.data)
            
            return Response(data={"message" : "updated" , "data" : request.data},status=status.HTTP_200_OK)
                    
        except Vendor.DoesNotExist:
            return Response(data={"message" : "vendor does not exist"},status=status.HTTP_404_NOT_FOUND)    
            
        except Exception as e:
            return Response(data={"message" : "validation error" , "error" : str(e)},status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
    def delete(self,request,pk=None):
        
        try:
            vendor = Vendor.objects.get(id = pk)
            vendor.delete()
            
            return Response(data={"message" : "deleted vendor"},status=status.HTTP_200_OK)
            
        except Vendor.DoesNotExist:
            return Response(data={"message" : "vendor does not exist"} ,status=status.HTTP_404_NOT_FOUND)