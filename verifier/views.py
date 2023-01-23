from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib import messages
from django.core.mail import send_mail, EmailMessage
from django.conf import settings
from django.template.loader import render_to_string
from email_validator import validate_email, EmailNotValidError

from .models import EmailList

# Create your views here.


def home(request):
    email_list = EmailList.objects.values_list()

    if request.method == "POST":
        email = request.POST.get('email')
        context = {
            'email': email
        }
        try:
            validate = validate_email(email)
            subject = 'Verify Your Email Address'
            val = {
                'site_url': settings.SITE_URL,
                'subject': subject,
            }

            message = 'Verify Your Email Address here!'
            html = render_to_string('verify.html', val)
            list_of_email = []

            for i in email_list:
                list_of_email.append(i[1])

            if email not in list_of_email:
                list_of_email.append(email)
                EmailList.objects.create(email=email)
                send_mail(
                    subject=subject,
                    message=message,
                    from_email=settings.EMAIL_HOST_USER,
                    recipient_list=[email],
                    fail_silently=False,
                    html_message=html
                )

                messages.success(request, f'{email} is a valid email address')

            else:
                messages.warning(request, f'{email} has already been validated')

            return render(request, 'index.html', context)

        except EmailNotValidError as e:
            messages.warning(request, e)

            return render(request, 'index.html')

    return render(request, 'index.html')
