from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class CustomUser(AbstractUser):
    ROLE_CHOICES = (
        ('admin', 'Admin'),
        ('user', 'User'),
    )
    role = models.CharField(choices=ROLE_CHOICES, default='user', max_length=10)

class Tag(models.Model):
    tag = models.CharField(max_length=16)
    