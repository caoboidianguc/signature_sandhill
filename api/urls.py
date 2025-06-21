from django.urls import path
from . import views


app_name = 'api'
urlpatterns = [
    path('tech/', views.AllTechView.as_view(), name='alltech_api'),
    path('tech/<int:pk>', views.SingleTech.as_view(), name='single_tech'),
    path('khach/', views.AllKhachView.as_view(), name='allkhach_api'),
    path('khach/<int:pk>', views.SingleKhach.as_view(), name='single_khach'),
    path('services/', views.ServiceView.as_view(), name='services_api'),
]

