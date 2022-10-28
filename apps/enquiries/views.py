from django.core.mail import send_mail
from pstore.settings.development import DEFAULT_FROM_EMAIL
from rest_framework import permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response

from .models import Enquiry

# Create your views here.


@api_view(["POST"])
@permission_classes([permissions.AllowAny])
def send_enquiry_email(request):
    data = request.data
    try:
        subject = data["subject"]
        name = data["name"]
        email = data["email"]
        message = data["message"]
        from_email = data["email"]
        recipient_list = [DEFAULT_FROM_EMAIL]
        send_mail(
            subject,
            message,
            from_email,
            recipient_list,
            fail_silently=True,
        )
        enquiry = Enquiry(name=name, email=email, subject=subject, message=message)
        print("Enquiry: ", enquiry)
        enquiry.save()
        return Response({"success": "Your Enquiry was successfully submited"})
    # mail = EmailMessage(subject=subject, to=recipient_list, from_email=from_email, body=message)
    # mail.send(fail_silently=True)
    # enquiry = Enquiry(name=name, email=email, subject=subject, message=message)
    # enquiry.save()
    #     print("SUCCESS")
    #     return Response({"success": "Your Enquiry was successfully submited"})
    except ValueError as e:
        print("FAIL", e)
        return Response({"fail": "Enquiry was not send. Please Try Again."})
