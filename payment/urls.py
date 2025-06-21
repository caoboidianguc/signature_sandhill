from django.urls import path
from payment import views


app_name = 'payment'
urlpatterns = [
    path('success_checkout/', views.SuccessCheckoutView.as_view(), name='success_checkout'),
    path('cancel_checkout/', views.CancelCheckoutView.as_view(), name='cancel_checkout'),
    path('all_services_checkout/', views.ServicesPaymentView.as_view(), name='services_for_checkout'),
    path('multiple_checkout_session/', views.CreateMultipleCheckoutSessionView.as_view(), name='multi_checkout_session'),
    path('webhooks/stripe/', views.stripe_webhook, name='stripe-webhook'),
]