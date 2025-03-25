from celery import shared_task
from django.core.mail import send_mail
import random

@shared_task
def send_otp_email(user_email, otp):
    #otp = random.randint(100000, 999999)
    subject = "Your OTP Code"
    message = f"Your OTP is {otp}."
    from_email = "prakharchauhan816@gmail.com"
    recipient_list = [user_email]

    send_mail(subject, message, from_email, recipient_list)
    return f"OTP {otp} sent to {user_email}"