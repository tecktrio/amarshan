from rest_framework import serializers

from API.models import Donations
from API.models import Featured
from API.models import Users
from API.models import Products

class DonationContent_Serializer(serializers.ModelSerializer):
    class Meta:
        model = Donations
        fields = "__all__"
class FeaturedContent_Serializer(serializers.ModelSerializer):
    class Meta:
        model = Featured
        fields = "__all__"
class User_Serializer(serializers.ModelSerializer):
    class Meta:
        model= Users
        fields = '__all__'
        
class Product_Serializer(serializers.ModelSerializer):
    class Meta:
        model=Products
        fields = '__all__'