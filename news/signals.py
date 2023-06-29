from django.contrib.auth.models import Group, User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth import get_user_model
from django.shortcuts import redirect

from .utils.mails import send_welcome_email
from .utils.mails import send_subscribe_mail

from .models import Subscription
# from .forms import SubscribeForm


@receiver(post_save, sender=get_user_model())
def add_user_to_common_group(sender, instance, created, **kwargs):
    if created:
        common_group, _ = Group.objects.get_or_create(name='common')
        instance.groups.add(common_group.id)


# @receiver(post_save, sender=User)
# def send_welcome_email_on_creation(sender, instance, created, **kwargs):
#     if created:
#         send_welcome_email(instance.email)


# @receiver(post_save, sender=Subscription)
# def subscription_created(sender, instance, created, **kwargs):
#     if created:
#         category_name = instance.category.name_category
#         send_subscribe_mail(instance.user, category_name)
#     return redirect('posts_list')
