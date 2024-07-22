from chat.models import Chat
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def post_save_user(sender, instance, created, **kwargs):
    if not getattr(instance, "chat", None):
        Chat.objects.create(user=instance)
