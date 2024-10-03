from django.shortcuts import render

# Create your views here.
from rest_framework import generics,permissions,viewsets
from rest_framework import status
from rest_framework.views import APIView
from .models import *
from django.contrib.auth.models import User
from .serializers import *
from django.utils import timezone
from dateutil.relativedelta import relativedelta
from django.db.models import Count,Avg
from rest_framework.response import Response


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

class AnalyticsView(APIView):
    permission_classes = (permissions.IsAuthenticated)

    def get(self,request):
        now = timezone.now()
        last_month = now - relativedelta(months=1)
        contacts_count =Contact.objects.filter(user=request.user).count()
        properties_count = Property.objects.filter(user=request.user).count()
        appointments_count = Appointment.objects.filter(User=request.user,date_time__gte=last_month)
        tasks_completed =Task.objects.filter(user=request.user,status='done',updated_at__gte=last_month)
        lead_status_distribution = Contact.objects.filter(user=request.user).values('lead_status').annotate(count=Count('id'))
        property_type_distribution = Property.objects.filter(user=request.user).values('property_type').annotate(count=Count('id'))
        avg_property_price = Property.objects.filter(user=request.user).aggregate(Avg('price'))['price__avg']

        return Response({
            'contacts_count': contacts_count,
            'properties_count': properties_count,
            'appointments_last_month': appointments_count,
            'tasks_completed_last_month': tasks_completed,
            'lead_status_distribution': lead_status_distribution,
            'property_type_distribution': property_type_distribution,
            'avg_property_price': avg_property_price
        })

class DocumentViewset(viewsets.ModelViewSet):
    serializer_class = DocumentSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get_queryset(self):
        return Document.objects.filter(user=self.request.user)
    
    def perform_create(self,serializer):
        return serializer.save(user=self.request.user)