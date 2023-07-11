import datetime
from celery import shared_task
from django.conf import settings
from django.template.loader import render_to_string
from django.utils import timezone

from .models import Post, Subscription
from django.core.mail import EmailMultiAlternatives


@shared_task
def week_send_email_task():
    today = timezone.make_aware(datetime.datetime.now(), timezone.get_current_timezone())
    last_week = today - datetime.timedelta(days=7)
    posts = Post.objects.filter(created_at__gte=last_week)
    categories = set(posts.values_list('category__name_category', flat=True))
    subscribers = set(Subscription.objects.filter(category__name_category__in=categories).values_list('email',
                                                                                                      flat=True))
    html_content = render_to_string(
        'news/daily_post.html',
        {
            'link': settings.SITE_URL,
            'posts': posts,
        }
    )
    msg = EmailMultiAlternatives(
        subject='Статьи за неделю',
        body='',
        from_email=settings.EMAIL_HOST_USER_FULL,
        bcc=subscribers
    )
    msg.attach_alternative(html_content, 'text/html')
    msg.send()