from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from django.db.models.signals import post_save, m2m_changed
from django.dispatch import receiver

from .models import Post, PostCategory


from .utils.mails import send_article_notifications


@receiver(post_save, sender=get_user_model())
def add_user_to_common_group(instance, created, **kwargs):
    if created:
        common_group, _ = Group.objects.get_or_create(name='common')
        instance.groups.add(common_group.id)


@receiver(m2m_changed, sender=PostCategory)
def send_notification_email_on_post_save(instance, action, **kwargs):
    if action == 'post_add':
        post_id = Post.objects.get(id=instance.id)
        send_article_notifications(post_id.id)