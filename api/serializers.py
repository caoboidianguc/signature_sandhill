from rest_framework import serializers
from ledger.models import Technician, Khach, Service
import bleach
from datetime import timedelta, date
import datetime


      
        

class ServiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Service
        fields = ('service', 'price', 'time_perform','description')
        extra_kwargs = {
            'price': {'min_value': 1}
        }

class TechnicSerializer(serializers.ModelSerializer):
    services = ServiceSerializer(many=True, read_only=True)
    class Meta:
        model = Technician
        fields = '__all__'
        

class KhachSerializer(serializers.ModelSerializer):
    services = ServiceSerializer(many=True, read_only=True)
    technician = TechnicSerializer()
    class Meta:
        model = Khach
        fields = '__all__'
        
