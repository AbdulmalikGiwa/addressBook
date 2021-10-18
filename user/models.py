from django.contrib.auth.models import AbstractUser
from django.db import models
from safedelete.models import SafeDeleteModel


class User(AbstractUser, SafeDeleteModel):
    first_name = models.CharField(blank=False, max_length=40)
    last_name = models.CharField(blank=False, max_length=40)
    email = models.EmailField(blank=False, null=False, unique=True)
    phone = models.CharField(blank=True, max_length=255)
    username = None

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []