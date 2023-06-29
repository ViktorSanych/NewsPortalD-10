import os
from django.core.mail import send_mail


def send_welcome_email(email):
    subject = "Добро пожаловать!"
    message = "Добро пожаловать на наш сайт!"
    from_email = os.getenv('EMAIL_HOST_USER_FULL')
    recipient_list = [email]
    send_mail(subject, message, from_email, recipient_list)


def send_subscribe_mail(user_email, category_name):
    subject = f'Вы подписались на категорию "{category_name}"!'
    message = f'Здравствуйте!\n\nВы успешно подписались на новости в категории "{category_name}".'
    from_email = os.getenv('EMAIL_HOST_USER_FULL')
    recipient_list = [user_email]
    send_mail(subject, message, from_email, recipient_list)