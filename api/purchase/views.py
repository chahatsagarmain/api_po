from rest_framework.views import APIView
from .models import PurchaseOrder
from .serializers import PurchaseSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from rest_framework.parsers import MultiPartParser , FormParser , JSONParser
from datetime import datetime , timedelta
# Create your views here.

class PurchaseViews(APIView):
    permission_classes = [IsAuthenticated,]
    parser_classes = [JSONParser,FormParser,MultiPartParser]

    def get(self,request,format=None):
        
        query_set = PurchaseOrder.objects.all()
        serialized_data = PurchaseSerializer(query_set,many=True)
        print(query_set)
        return Response(data = {"data" : serialized_data.data},status=status.HTTP_200_OK)
    
    def post(self,request,format=None):
        #create a new order with no vendor 
        data = request.data.copy()
        data["order_date"] = datetime.now().strftime('%Y-%m-%d')
        #temporary solution to delievery date
        delivery_date = datetime.now() + timedelta(days=7)
        data["delivery_date"] = delivery_date.strftime('%Y-%m-%d')
        data["status"] = "pending"
        
        try:
            serialized = PurchaseSerializer(data=data)
            serialized.is_valid(raise_exception=True)
            serialized.save()

        except Exception as e:
            print(e)
            return Response({"message" : "validation error"},status=status.HTTP_400_BAD_REQUEST)
        return Response({"data" : serialized.data})
    
class PurchaseViewsById(APIView):
    permission_classes = [IsAuthenticated,]
    parser_classes = [JSONParser,FormParser,MultiPartParser]
    
    def get(self, request , pk , format=None):
        
        try:
            po = PurchaseOrder.objects.filter(pk=pk)
            serialized = PurchaseSerializer(po,many=True)
            return Response({"data" : serialized.data},status=status.HTTP_200_OK)
        except PurchaseOrder.DoesNotExist:
            return Response({"message" : "purchase order does not exist"},status=status.HTTP_404_NOT_FOUND)
    
    def delete(self, request, pk, format=None):
        try:
            po = PurchaseOrder.objects.get(pk=pk)
        except PurchaseOrder.DoesNotExist:
            return Response({"message": "Purchase order does not exist"}, status=status.HTTP_404_NOT_FOUND)

        po.delete()
        return Response({"message": "deleted"}, status=status.HTTP_200_OK)

    def put(self,request,pk,fromat=None):
        try:
            po = PurchaseOrder.objects.get(pk=pk)
            

        except PurchaseOrder.DoesNotExist:
            return Response({"message : po does not exist"},status=status.HTTP_404_NOT_FOUND)