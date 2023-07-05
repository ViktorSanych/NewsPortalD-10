import os
from django.core.mail import send_mail

from news.models import Subscription, PostCategory, Post

from django.urls import reverse
from django.template.loader import render_to_string


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


def send_article_notifications(post_id):
    post = Post.objects.get(id=post_id)
    post_categories = PostCategory.objects.filter(post=post)
    category_ids = post_categories.values_list('category', flat=True)
    subscribers = Subscription.objects.filter(category_id__in=category_ids)
    for subscriber in subscribers:
        email = subscriber.email
        from_email = os.getenv('EMAIL_HOST_USER_FULL')

        # Получение начала статьи (40 символов)
        post_start = post.text[:40]

        # Получение ссылки на статью
        post_url = reverse('post_detail', args=[post.pk])

        # Генерация контекста для шаблона письма
        context = {'post_start': post_start, 'post_url': post_url}

        # Генерация HTML-содержимого письма с помощью шаблона
        html_content = render_to_string('news/post_notification.html', context)
        recipient_list = [email]
        # Отправка письма
        send_mail('Новая статья', '', from_email, recipient_list, html_message=html_content)