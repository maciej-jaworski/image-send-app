import uuid

from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4)

    @property
    def is_staff(self):
        return self.is_superuser

    @is_staff.setter
    def is_staff(self, value):
        return

    def __str__(self):
        return self.get_full_name() or self.email or self.username
