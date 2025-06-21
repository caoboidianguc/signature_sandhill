from django.urls import path, re_path, include
from ledger import views, complimentary
from django.conf import settings
from django.conf.urls.static import static


app_name = 'ledger'
urlpatterns = [
    path('', views.CustomerVisit.as_view(), name="index"),
    path('ledger/privacy_policy/', views.PrivacyPolicy.as_view(), name="privacy"),
    path('ledger/contact/', views.Contact.as_view(), name="contact"),
    path('ledger/', views.AllEmployee.as_view(), name="all_employee"),
    path('ledger/add_employee/', views.EmpCreate.as_view(), name="add_employee"),
    path('ledger/register/', views.TaoTaiKhoan.as_view(), name="register"),
    path('ledger/services/', views.AllServices.as_view(), name="services"),
    path('ledger/services/detail/<int:pk>/', views.ServiceDetail.as_view(), name="service_detail"),
    path('ledger/services/add_services/', views.AddService.as_view(), name="add_service"),
    path('ledger/update_employee_status/', views.UpdateTech.as_view(), name="update_tech_status"),
    path('ledger/tech_vacation/<int:pk>/', views.TechVacationView.as_view(), name="vacation"),
    path('ledger/chat_room/<int:pk>/', views.ChatView.as_view(), name="chat_room"),
    path('ledger/chat_room/detail/<int:pk>/', views.ChatDetailView.as_view(), name="chat_detail"),
    path('ledger/user_chat_room/', views.UserChatView.as_view(), name="user_chat_room"),
    path('ledger/chat/<int:pk>/create/', views.ChatCreateView.as_view(), name="chat_create"),
    path('ledger/user_chat_create/', views.UserChatCreateView.as_view(), name="user_chat_create"),
    path('ledger/user_chat_room/detail/<int:pk>/', views.UserChatDetailView.as_view(), name="user_chat_detail"),
    path('ledger/walkin/', views.ClientWalkinView.as_view(), name='walkin' ),
    path('ledger/chat/<int:chat_id>/like/', views.ChatLikeView.as_view(), name='chat_like'),
    path('ledger/chat_detail/<int:chat_id>/like/', views.chatDetailLike, name='chat_detail_like'),
    path('ledger/chat_user/<int:chat_id>/like/', views.ChatUserLikeView.as_view(), name='user_chat_like'),
    path('ledger/chat/<int:pk>/delete/', views.chat_delete, name='chat_delete'),
    path('ledger/service/info/<str:category>/', views.services_info, name='service_info'),
    
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

urlpatterns += [
    path('ledger/supply/create/', views.SupplyCreateView.as_view(), name='supply_create'),
    path('ledger/supply/all/', views.AllSupply.as_view(), name='all_supplies'),
    path('ledger/supply/<int:supply_id>/wanted/', views.supplyWanted, name="supply_is_wanted"),
    path('ledger/supply/<int:pk>/delete/', views.supplyDelete, name='supply_delete'),
    path('ledger/employee/<int:pk>/', views.EmployeeBio.as_view(), name='employee_bio'),
    
    path('ledger/complimentaries/', complimentary.ComplimentaryListView.as_view(), name='complimentary_list' ),
    path('ledger/add/complimentary/', complimentary.ComplimentaryCreateView.as_view(), name='add_complimentary' ),
    path('ledger/complimentary/<int:pk>/offer/', complimentary.complimentary_is_available, name='complimentary_available' ),
    path('ledger/complimentary/<int:pk>/here/', complimentary.IamHereView.as_view(), name='iam_here' ),
    path('ledger/complimentary/client/<int:pk>/favorite/', complimentary.ClientFavoriteView.as_view(), name='client_favorite' ),
    
]