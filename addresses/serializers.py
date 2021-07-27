from rest_framework import serializers
from .models import City, District, Address

class CitySerializer(serializers.ModelSerializer):
    class Meta:
        model = City
        fields = ('id', 'name')  

class DistrictSerializer(serializers.ModelSerializer):
    city = CitySerializer(read_only=True)
    class Meta:
        model = District
        fields = ('id', 'name', 'city')  

class AddressSerializer(serializers.ModelSerializer):
    city = CitySerializer(read_only=True)
    district = DistrictSerializer(read_only=True)
    class Meta:
        model = Address
        fields = ('id', 'city', 'district', 'section', 'address')  