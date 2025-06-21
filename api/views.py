from django.shortcuts import render
from rest_framework import generics
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import TechnicSerializer, KhachSerializer, ServiceSerializer
from ledger.models import Technician, Khach, Service



class AllTechView(generics.ListCreateAPIView):
    queryset = Technician.objects.all()
    serializer_class = TechnicSerializer

# generics.RetrieveUpdateAPIView => GET PUT PATCH
class SingleTech(generics.RetrieveUpdateAPIView):
    queryset = Technician.objects.all()
    serializer_class = TechnicSerializer

class SingleKhach(generics.RetrieveUpdateAPIView):
    queryset = Khach.objects.all()
    serializer_class = KhachSerializer
    
class AllKhachView(generics.ListCreateAPIView):
    queryset = Khach.objects.all()
    serializer_class = KhachSerializer
    # search_fields=['full_name']   work with viewsets.ModelViewSet
    

# generics.ListCreateAPIView => get, post
class ServiceView(generics.ListAPIView):
    queryset = Service.objects.all()
    serializer_class = ServiceSerializer
    
    
