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



class StudentRecord(models.Model):
    lrn = models.CharField(max_length=12)  # Keep as CharField but validate as numeric
    last_name = models.CharField(max_length=50)
    first_name = models.CharField(max_length=50)
    middle_name = models.CharField(max_length=50, blank=True, null=True)

    def __str__(self):
        return f"{self.lrn} - {self.last_name}, {self.first_name}"