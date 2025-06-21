from django.shortcuts import render
from django.views.generic import TemplateView, ListView
from django.views import View
from django.http import JsonResponse, HttpResponse, HttpResponseBadRequest
from django.http import JsonResponse, HttpResponse
from django.urls import reverse_lazy
import stripe, os
from ledger.models import Service, Technician
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from ledger.views import contactEmail
from datetime import datetime
from django.utils import timezone

stripe.api_key = os.environ.get('stripe_secret_key')

class ServicesPaymentView(TemplateView):
    template_name = 'payment/services_payment.html' 
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['services'] = Service.objects.all
        context['techs'] = Technician.objects.exclude(name='anyOne')
        return context

class SuccessCheckoutView(TemplateView):
    template_name = 'payment/success_checkout.html'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        session_id = self.request.GET.get('session_id')
        try:
            
            session = stripe.checkout.Session.retrieve(session_id, expand=['line_items', 'payment_intent.charges'])
            client_name = session['customer_details']['name']
            client_email = session['customer_details']['email']
            line_items = session['line_items']['data']
            tech_id = session.metadata.get('technician_id', 'Unknown')
            total = 0
            payment_intent = session.get('payment_intent', {})
            charges = payment_intent.get('charges', {}).get('data', [])
            
            if session['payment_status'] == 'paid' and charges:
                charge = charges[0]
                payment_date = datetime.fromtimestamp(charge.get('created', 0))
                context['today'] = payment_date.strftime("%B %d, %Y")
            else:
                payment_date = datetime.fromtimestamp(session.get('created', 0))
                context['today'] = payment_date.strftime("%B %d, %Y")
            
            services = []
            for item in line_items:
                description = item['description']
                total_amount = item['amount_total'] / 100
                total += total_amount
                services.append({
                    'description': description,
                    'total_price': total_amount,
                })
            context['client_name'] = client_name
            context['services'] = services
            context['total'] = total
            context['tech'] = Technician.objects.get(id=tech_id)
            payment_time_str = timezone.now().strftime("%B %d, %Y, at %I:%M %p %Z")
            email_body = {
                'client_email': client_email,
                'client_name': client_name,
                'services': services,
                'total_amount': total,
                'currency': session['currency'],
                'payment_time': payment_time_str,
                # 'tax': tax,
                'total_amount': total,
                'tech': Technician.objects.get(id=tech_id),
            }
            body = render_to_string('payment/confirmation_email.html', email_body)
            email = EmailMessage(
                subject='Payment Confirmation',
                body=body,
                from_email=contactEmail,
                to=[client_email],
            )
            email.content_subtype = 'html'
            email.send()
                
        except Exception as e:
            print(f"Unexpected error: {e}")
            context['error'] = "An unexpected error occurred."
        return context
  
class CancelCheckoutView(TemplateView):
    template_name = 'payment/cancel_checkout.html'
    
        
class CreateMultipleCheckoutSessionView(View):
    def post(self, request, *args, **kwargs):
        service_ids = request.POST.getlist('service_ids')
        services = Service.objects.filter(id__in=service_ids)
        tech_id = request.POST.get('technician_id')
        try:
            line_items = []
            for service in services:
                if not service.stripe_product_id:
                    return JsonResponse({'error': 'Service does not have a Stripe product ID'}, status=400)
                
                line_items.append({
                    'price_data': {
                        'currency': 'usd',
                        'product': service.stripe_product_id,
                        'unit_amount': int(service.price * 100),  # Convert to cents
                    },
                    'quantity': 1,
                })
                
            session = stripe.checkout.Session.create(
                payment_method_types=['card'],
                line_items=line_items,
                mode='payment',
                success_url=request.build_absolute_uri(reverse_lazy('payment:success_checkout')) + '?session_id={CHECKOUT_SESSION_ID}',
                cancel_url=request.build_absolute_uri(reverse_lazy('payment:cancel_checkout')),
                # automatic_tax={'enabled': True},
                metadata={
                    'technician_id': tech_id,
                }
                
            )
            return redirect(session.url, code=303)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)


# https://docs.stripe.com/checkout/fulfillment?lang=python

def fulfill_checkout(session):
    session_data = stripe.checkout.Session.retrieve(session['id'], expand=['line_items'])
    client_email = session_data['customer_details'].get('email')
    client_name = session_data['customer_details']['name']
    line_items = session_data['line_items']['data']
    total = session_data['amount_total'] / 100  # Convert cents to dollars
    total = session_data['amount_total'] / 100  # Convert cents to dollars
    currency = session_data['currency']
    tech_id = session_data['metadata'].get('technician_id', 'Unknown')
    tech = Technician.objects.get(id=tech_id) if tech_id != 'Unknown' else None
    # tax = session_data.get('total_details', {}).get('amount_tax', 0) / 100  # Convert cents to dollars
    services = []
    for item in line_items:
        description = item['description']
        total_amount = item['amount_total'] / 100
        services.append({
            'description': description,
            'total_price': total_amount,
        })


    payment_time_str = timezone.now().strftime("%B %d, %Y, at %I:%M %p %Z")
    context = {
        'client_email': client_email,
        'client_name': client_name,
        'services': services,
        'total_amount': total,
        'currency': currency,
        'payment_time': payment_time_str,
        # 'tax': tax,
        'total_amount': total,
        'tech': tech,
    }
    body = render_to_string('payment/confirmation_email.html', context)
    email = EmailMessage(
        subject='Payment Confirmation',
        body=body,
        from_email=contactEmail,
        to=[client_email],
    )
    email.content_subtype = 'html'
    email.send()

# stripe listen --forward-to localhost:8000/payment/webhooks/stripe/
# checkout.session.completed asigned from dashboard stripe
@csrf_exempt
def stripe_webhook(request):
    payload = request.body
    sig_header = request.META['HTTP_STRIPE_SIGNATURE']
    event = None

    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, os.environ.get('endpoint_secret')
        )
    except ValueError as e:
        return HttpResponse(status=400)
    except stripe.error.SignatureVerificationError as e:
        return HttpResponse(status=400)

    if event['type'] == 'checkout.session.completed':
        session = event['data']['object']
        fulfill_checkout(session)
    return HttpResponse(status=200)
