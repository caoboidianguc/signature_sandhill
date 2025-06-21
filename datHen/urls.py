from django.urls import path
from datHen import views

app_name = "datHen"
urlpatterns = [
    path('all/', views.DatHenView.as_view(), name='listHen' ),
    path('get_client/', views.FindClient.as_view(), name='find_client' ),
    path('user_get_client/', views.UserFindClient.as_view(), name='user_find_client' ),
    path('existclient/<int:pk>/', views.ExistPickTech.as_view(), name='exist_found' ),
    path('first_step/', views.FirstStep.as_view(), name='first_step' ),
    path('third_step/', views.ThirdStep.as_view(), name='third_step' ),
    path('tech/<int:pk>/', views.Second.as_view(), name='technician_detail' ),
    path('tech_exist/<int:pk>/', views.ExistSecond.as_view(), name='technician_detail_exist' ),
    path('third_step_exist/', views.ExistThirdStep.as_view(), name='third_step_exist' ),
    path('services_choice/', views.ChoiceServicesView.as_view(), name='service_choice' ),
    path('services_choice_exist/', views.ChoiceServicesExistView.as_view(), name='service_choice_exist' ),
    path("cancel_confirm/<int:pk>/", views.CancelKhachVisit.as_view(), name='cancel_khachvisit' ),
    path("client/cancel_confirm/<int:pk>/", views.CancelViewConfirm.as_view(), name='cancel_confirm' ),
    path("client_detail/<int:pk>/", views.ClientDetailView.as_view(), name='client_detail' ),
    path("client/visit_detail/<int:pk>/", views.VisitDetailView.as_view(), name='visit_detail'),
    path("user/scheduler/", views.ScheduleViewUser.as_view(), name='schedule_user'),
    path("user/scheduler/get_client/", views.schedule_get_client, name='schedule_get_client'),
    
]

