import os
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from django.core.mail import send_mail
from django.db.models.signals import post_save, m2m_changed
from django.dispatch import receiver
from django.template.loader import render_to_string
from django.urls import reverse

from .models import Post, Subscription, PostCategory


from .utils.mails import send_article_notifications


@receiver(post_save, sender=get_user_model())
def add_user_to_common_group(sender, instance, created, **kwargs):
    if created:
        common_group, _ = Group.objects.get_or_create(name='common')
        instance.groups.add(common_group.id)


@receiver(m2m_changed, sender=Post.category.through)
def send_notification_email_on_post_save(sender, instance, action, pk_set, **kwargs):
    if action == 'post_add':
        post_id = Post.objects.filter(instance.id)
        send_article_notifications(post_id)
        # post_categories =
        # categories_ids = post_categories.values_list('category', flat=True)
        # print(categories_ids)
        # subscribers = Subscription.objects.filter(category_id__in=categories_ids)
        # for subscriber in subscribers:
        #     email = subscriber.email
        #     from_email = os.getenv('EMAIL_HOST_USER_FULL')
        #
        #     # Получение начала статьи (40 символов)
        #     post_start = instance.text[:40]
        #
        #     # Получение ссылки на статью
        #     post_url = reverse('post_detail', args=[instance.pk])
        #
        #     # Генерация контекста для шаблона письма
        #     context = {'post_start': post_start, 'post_url': post_url}
        #
        #     # Генерация HTML-содержимого письма с помощью шаблона
        #     html_content = render_to_string('news/post_notification.html', context)
        #     recipient_list = [email]
        #     # Отправка письма
        #     send_mail('Новая статья', '', from_email, recipient_list, html_message=html_content)
