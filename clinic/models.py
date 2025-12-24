from django.db import models  
from django.contrib.auth.models import AbstractUser, Group, Permission

# User Roles
USER_ROLES = (
    ('admin', 'Admin'),
    ('doctor', 'Doctor'),
    ('receptionist', 'Receptionist'),
)

class CustomUser(AbstractUser):
    role = models.CharField(max_length=20, choices=USER_ROLES, default='receptionist')

    # Fix group and permission conflicts
    groups = models.ManyToManyField(Group, related_name="customuser_groups", blank=True)
    user_permissions = models.ManyToManyField(Permission, related_name="customuser_permissions", blank=True)

    def __str__(self):
        return f"{self.username} - {self.role}"

class Patient(models.Model):
    GENDER_CHOICES = [
        ('M', 'Male'),
        ('F', 'Female'),
        ('O', 'Other'),
    ]

    name = models.CharField(max_length=100)
    age = models.IntegerField()
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, default='M')  # Gender field
    contact_number = models.CharField(max_length=15)
    email = models.EmailField(unique=True)
    address = models.TextField(blank=True, null=True)  # Address field
    medical_history = models.TextField(blank=True, null=True)  # Medical history field
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

# ✅ Doctor Model
class Doctor(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    specialization = models.CharField(max_length=150)
    phone = models.CharField(max_length=15, blank=True, null=True)
    email = models.EmailField()

    def __str__(self):
        return f"Dr. {self.first_name} {self.last_name}"

# ✅ Blog Model
class Blog(models.Model):
    title = models.CharField(max_length=200)
    image = models.ImageField(upload_to='blog_images/', null=True, blank=True)  # ✅ Image field
    author = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    content = models.TextField()

    def __str__(self):
        return self.title
