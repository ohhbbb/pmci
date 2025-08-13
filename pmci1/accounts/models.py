from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    ROLE_CHOICES = [
        ('admin', 'Admin'),
        ('finance', 'Finance'),
        ('registrar', 'Registrar'),
    ]
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='admin')

    def __str__(self):
        return f"{self.username} ({self.role})"
    
class AddUser(models.Model):
    username = models.CharField(max_length=150, unique=True)
    password = models.CharField(max_length=128)
    email = models.EmailField(unique=True)
    role = models.CharField(max_length=20, choices=CustomUser.ROLE_CHOICES)

    def __str__(self):
        return f"{self.username} ({self.role})"

    class Meta:
        verbose_name = 'Add User'
        verbose_name_plural = 'Add Users'