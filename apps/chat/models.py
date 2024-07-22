import uuid

from django.conf import settings
from django.db import models


def image_upload_path(instance, filename):
    return f"schedules/{uuid.uuid4()}/{filename}"


class Image(models.Model):
    external_id = models.PositiveIntegerField(null=True, editable=False)
    image_file = models.FileField(upload_to=image_upload_path)


class Message(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    text = models.CharField(max_length=1024)  # TODO: max length requirements
    image = models.ForeignKey(Image, on_delete=models.CASCADE)

    class Meta:
        ordering = ("created_at",)


class Chat(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    messages = models.ManyToManyField(Message, related_name="chats")
