from .models import KhachVisit
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.urls import reverse_lazy
import logging


contactEmail = "signature.sandhill@gmail.com"
chuDe = "Signature Nails Sandhill Confirm schedule"
tenSpa = "Signature Nails Sandhill"
address = "163 Forum Dr, #5 Columbia, SC 29229"

def saveKhachVisit(client, date, time, services, tech, status):
    try:
        khachvisit = KhachVisit(client=client, day_comes=date, time_at=time,technician=tech, status=status)
        khachvisit.save()
        khachvisit.services.set(services)
        khachvisit.total_spent = sum(dv.price for dv in services)
        khachvisit.save(update_fields=['total_spent'])
    except ValueError as e:
        print(f"Error saving KhachVisit: {e}")
        return

def cancelKhachVisit(client):
    try:
        visit = KhachVisit.objects.filter(client=client)
        for item in visit:
            item.delete()
    except ValueError as e:
        print(f"Error retrived visit: {e}")
        return

logging.getLogger(__name__)

def sendEmailConfirmation(request, client):
    try:
        email_body = {
                    'client': client,
                    'cancel_link': cancel_visit(request, client.id),
                    
                }
        body = render_to_string('datHen/email_confirm_dathen.html', email_body)
        email = EmailMessage(
            subject='Appointment Confirmation',
            body=body,
            from_email=contactEmail,
            to=[client.email],
        )
        email.content_subtype = 'html'
        email.send()
        logging.info(f"Email sent to {client.email} for appointment confirmation.")
    except Exception as e:
        logging.error(f"Error sending email to {client.email}: {str(e)}")

def cancel_visit(request, id):
    url = reverse_lazy('datHen:cancel_confirm', kwargs={'pk': id})
    link = request.build_absolute_uri(url)
    return link
