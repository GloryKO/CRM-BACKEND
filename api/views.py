from django.shortcuts import render

# Create your views here.
from rest_framework import generics,permissions,viewsets
from rest_framework import status
from .models import *
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

class ContactViewSet(viewsets.ModelViewSet):
    serializer_class = ContactSerializer
    permission_classes = (permissions.IsAuthenticated,)

    #override the default query_set to assign only contacts associated to the currenly authenticated user
    def get_queryset(self):
        return Contact.objects.filter(user=self.request.user)
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class PropertyViewSet(viewsets.ModelViewSet):
    serializer_class = PropertySerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get_queryset(self):
        return Property.objects.filter(user=self.request.user)
    
    def perfrom_create(self,serializer):
        serializer.save(user=self.request.user)

class AppointmentViewSet(viewsets.ModelViewSet):
    serializer_class = AppointmentSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get_queryset(self):
        return Appointment.objects.filter(user=self.request.user)
    
    def perform_create(self,serializer):
        serializer.save(user=self.request.user)

class TaskViewSet(viewsets.ModelViewSet):
    serializer_class = TaskSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get_queryset(self):
        return Task.objects.filter(user=self.request.user)
    
    def perform_create(self,serializer):
        return serializer.save(user=self.request.user)

    