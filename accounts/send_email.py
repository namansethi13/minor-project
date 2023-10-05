from django.core.mail import send_mail
from django.conf import settings

def send_email(OTP , email):
        subject = "Welcome to the website , Here is your OTP for logging in to the website"
        message = f"OTP for logging in is: {OTP}  This OTP is valid for 5 minutes."
        email_from = settings.EMAIL_HOST_USER
        recipient_list = [email]
        send_mail( subject, message, email_from, recipient_list )