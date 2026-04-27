from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    USER_TYPE_CHOICES = (
        ('customer', 'Customer'),
        ('staff', 'Staff'),
        ('admin', 'Admin'),
    )
    user_type = models.CharField(max_length=20, choices=USER_TYPE_CHOICES, default='customer')
    role = models.CharField(max_length=50, blank=True, null=True) # for staff roles
    name = models.CharField(max_length=255, blank=True)

    # We will use this combined model for both customers and staff.
    # For customers: email is used for login. We will set username = email automatically.
    # For staff: username is used for login.
    
    def __str__(self):
        return f"{self.username} ({self.user_type})"
