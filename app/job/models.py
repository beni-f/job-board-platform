from django.db import models
from django.contrib.auth.models import AbstractUser


class CustomUser(AbstractUser):
    ROLE_CHOICES = (
        ('admin', 'Admin'),
        ('job_seeker', 'Job Seeker'),
        ('employer', 'Employer'),
    )
    role = models.CharField(choices=ROLE_CHOICES, default=None, max_length=10, null=True)
    email = models.EmailField(unique=True, null=False)

class Category(models.Model):
    name = models.CharField(max_length=16)

    def __str__(self):
        return self.name
    

class Job(models.Model):
    title = models.CharField(max_length=100, null=False)
    recruiter = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        related_name='jobs'
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        null=True,
        related_name='jobs'
    )
    description = models.TextField()
    salary = models.FloatField()
    location = models.CharField(max_length=100)
    date_posted = models.DateTimeField(auto_now_add=True)
    job_deadline = models.DateTimeField()


    def __str__(self):
        return self.title

