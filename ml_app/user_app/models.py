from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    birth_date = models.DateField(auto_now=False, null=True)