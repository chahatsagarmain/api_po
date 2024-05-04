from .models import CustomUser
from rest_framework.serializers import ModelSerializer
from rest_framework.authentication import get_user_model
User = get_user_model()

class UserSerializer(ModelSerializer):
    
    class Meta:
        model=CustomUser
        fields="__all__"
    
    def create(self , validated_data):
        if not validated_data.get("email",None) or not validated_data.get("password",None):
            return None
        
        user  = User.objects.create(
            email = validated_data.get("email"),
            username = validated_data.get("username"),
            password = validated_data.get("password")
        )
        user.set_password(raw_password=validated_data.get("password"))
        user.save()
    
        return user
    
    