from django.db import models
from django.contrib.auth.models import User #import the default User model

class UserProfile(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE,related_name='profile')
    phone_number = models.CharField(max_length=50,blank=True)
    address = models.TextField(blank=True)
    role=models.CharField(max_length=20,choices=[
        ('agent','Real Estate Agent'),
        ('manager','Manager'),
        ('admin','Admin')
    ],default='agent'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.username}'s profile"