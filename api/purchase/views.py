from rest_framework.views import APIView
from .models import PurchaseOrder
from .serializers import PurchaseSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from rest_framework.parsers import MultiPartParser , FormParser , JSONParser
from datetime import datetime , timedelta
from vendor.models import Vendor
# Create your views here.
date_format = '%Y-%m-%d'

class PurchaseViews(APIView):
    permission_classes = [IsAuthenticated,]
    parser_classes = [JSONParser,FormParser,MultiPartParser]

    def get(self,request,format=None):
        
        query_set = PurchaseOrder.objects.all()
        serialized_data = PurchaseSerializer(query_set,many=True)
        print(query_set)
        return Response(data = {"data" : serialized_data.data},status=status.HTTP_200_OK)
    
    def post(self,request,format=None):
        #post method will create a user with minimal data , data will be updaed with put method
        #create a new order with no vendor 
        data = request.data.copy()
        # datetime.strftime(datetime.today(),date_format)
        data["order_date"] = datetime.now()
        #temporary solution to delievery date
        print(data['order_date'])
        delivery_date = datetime.now() + timedelta(days=7)
        data["delivery_date"] = delivery_date
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
            
            data = request.data.copy()
            vendor = None
            print(data)
            tz_info = po.order_date.tzinfo
            
            if data['status'] == 'cancelled':
                po.status = data['status']
                if not po.vendor:
                    return Response({"message" : "status cant be assigned to purchase with no vendors"},status=status.HTTP_400_BAD_REQUEST)
                # case when vendor was assigned earlier but quality rating wasnt given
                # if vendor is assigned and quality rating is given , then the vendor should be filled
                if not vendor and po.vendor is not None:
                    vendor = Vendor.objects.get(pk=po.vendor)
                po.status = data['status']

            #first vendor assignment or new vendor assignment
            if (data['vendor'] and not po.vendor) or (data['vendor'] and po.vendor != data['vendor']):
                
                vendor = Vendor.objects.get(pk=data['vendor'])
                po.vendor = po.vendor or vendor
                po.issue_date = datetime.now(tz=tz_info)
                #new average_response
                response_time = datetime.now(tz=tz_info) - po.order_date
                num_orders = vendor.num_orders
                print(response_time)
                vendor.average_response_time = ((vendor.average_response_time * num_orders) + response_time.days) / (num_orders + 1)
                
            if data['quality_rating']:
                po.quality_rating = data['quality_rating']
                if not po.vendor:
                    return Response({"message" : "quality rating cant be assigned to purchase with no vendors"},status=status.HTTP_400_BAD_REQUEST)
                # case when vendor was assigned earlier but quality rating wasnt given
                # if vendor is assigned and quality rating is given , then the vendor should be filled
                if not vendor and po.vendor is not None:
                    vendor = Vendor.objects.get(pk=po.vendor)
                quality_rating = data['quality_rating']
                vendor.quality_rating_avg = ((vendor.quality_rating_avg * vendor.num_orders) + quality_rating) / (vendor.num_orders + 1)
            
            if data['status'] == 'completed':
                po.status = data['status']
                if not po.vendor:
                    return Response({"message" : "status cant be assigned to purchase with no vendors"},status=status.HTTP_400_BAD_REQUEST)
                # case when vendor was assigned earlier but quality rating wasnt given
                # if vendor is assigned and quality rating is given , then the vendor should be filled
                if not vendor and po.vendor is not None:
                    vendor = Vendor.objects.get(pk=po.vendor)
                delivery_date = datetime.now(tz=tz_info)
                print(delivery_date)
                if delivery_date <= po.delivery_date:
                    #on time dilivery 
                    print(1)
                    vendor.on_time_delivery_rate = ((vendor.on_time_delivery_rate * vendor.num_orders) + 1) / (vendor.num_orders + 1)
                    vendor.fulfillment_rate = ((vendor.fulfillment_rate*vendor.num_orders) + 1) / (vendor.num_orders + 1)
                    print(1)

                else:
                    vendor.on_time_delivery_rate = (vendor.on_time_delivery_rate * vendor.num_orders) / (vendor.num_orders + 1)
                    vendor.fulfillment_rate = (vendor.fulfillment_rate*vendor.num_orders) / (vendor.num_orders + 1)

            
            if "issues" in data and  data['issues']:
                print("2")
                # if no issues are reported then increment the fullfillment rate
                if not po.vendor:
                    return Response({"message" : "full fillment cant be assigned to purchase with no vendors"},status=status.HTTP_400_BAD_REQUEST)
                # case when vendor was assigned earlier but quality rating wasnt given
                # if vendor is assigned and quality rating is given , then the vendor should be filled
                if not vendor and po.vendor is not None:
                    vendor = Vendor.objects.get(pk=po.vendor)
                
                vendor.fulfillment_rate = ((vendor.fulfillment_rate * vendor.num_orders) + 1) / (vendor.num_orders + 1)
                
            else:
                if not po.vendor:
                    return Response({"message" : "full fillment cant be assigned to purchase with no vendors"},status=status.HTTP_400_BAD_REQUEST)
                # case when vendor was assigned earlier but quality rating wasnt given
                # if vendor is assigned and quality rating is given , then the vendor should be filled
                if not vendor and po.vendor is not None:
                    vendor = Vendor.objects.get(pk=po.vendor)
                
                vendor.fulfillment_rate = (vendor.fulfillment_rate * vendor.num_orders) / (vendor.num_orders + 1)

            po.save()
            if vendor : vendor.num_orders += 1
            if vendor : vendor.save()
            
            po_serialized = PurchaseSerializer(po)
            
            return Response({"message" : "updated" , "data" : po_serialized.data},status=status.HTTP_200_OK)
        
        except PurchaseOrder.DoesNotExist:
            return Response({"message" : "Purchase order does not exist"},status=status.HTTP_404_NOT_FOUND)

        except Vendor.DoesNotExist:
            return Response({"message" : "Vendor does not exist"},status=status.HTTP_404_NOT_FOUND)

        except Exception as e:
            return Response({"message" : "an error occured","error" : str(e)},status=status.HTTP_500_INTERNAL_SERVER_ERROR)