import os
from django.core.mail import send_mail


def send_welcome_email(email):
    subject = "Добро пожаловать!"
    message = "Добро пожаловать на наш сайт!"
    from_email = os.getenv('EMAIL_HOST_USER_FULL')
    recipient_list = [email]
    send_mail(subject, message, from_email, recipient_list)