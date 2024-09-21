from django.shortcuts import render

# Create your views here.
from rest_framework import generics,permissions
from rest_framework import status
from .models import UserProfile
from django.contrib.auth.models import User
from .serializers import *

class UserRegistrationView(generics.CreateAPIView):
    permission_classes = (permissions.AllowAny,)
    queryset = User.objects.all()
    serializer_class = UserRegistrationSerializer

class UserProfileView(generics.RetrieveUpdateAPIView):
    permission_classes = (permissions.IsAuthenticated,)
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer

    def get_object(self):
        """
        make sure an authenticated user only has access to their profile
        """
        return self.request.user.profile

class UserListView(generics.ListAPIView):
     permission_classes = (permissions.IsAdminUser,)
     queryset = User.objects.all()
     serializer_class = UserRegistrationSerializer
    