from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.parsers import FormParser , MultiPartParser
from rest_framework import status
from rest_framework.authentication import authenticate
from rest_framework.authtoken.models import Token
from .serializers import UserSerializer
from rest_framework.authentication import get_user_model
User = get_user_model()
# Create your views here.

class LoginApiView(APIView):
    parser_classes = [FormParser,MultiPartParser]
    permission_classes = [AllowAny,]
    
    def post(self , request , format = None):
        username = request.data.get("username",None)
        password = request.data.get("password",None)
        
        if not username or not password:
            return Response(data={"message" : "username or password missing"},status=status.HTTP_404_NOT_FOUND)
        
        user = authenticate(request , username=username , password=password)
        
        users = User.objects.all()
        
        if not user:
            return Response(data={"message" : "Wrong credentials"},status=status.HTTP_400_BAD_REQUEST)
        
        token = Token.objects.get_or_create(user = user)
      
        return Response(data={"message" : "logged in" , "response" : str(token[0])})
            
class RegisterApiView(APIView):
    parser_classes = [FormParser,MultiPartParser]
    permission_classes = [AllowAny,]
    
    def post(self , request , format=None):
        
        serialized_data = UserSerializer(data = request.data)
        
        try:
            serialized_data.is_valid(raise_exception=True)
            created_user = serialized_data.create(validated_data=serialized_data.validated_data)
            token = Token.objects.create(user=created_user)
            return Response(data={"message" : "user created" , "token" : str(token)},status=status.HTTP_201_CREATED)
            
        except Exception as e:
            return Response(data={"message" : str(e)},status=status.HTTP_400_BAD_REQUEST)
    
    