from rest_framework import serializers

from API.models import Donations
from API.models import Featured
from API.models import Users

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