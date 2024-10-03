from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .views import *
from rest_framework.routers import DefaultRouter
router = DefaultRouter()
router.register(r'contacts',ContactViewSet,basename='contact')
router.register(r'properties', PropertyViewSet, basename='property')
router.register(r'appointments', AppointmentViewSet, basename='appointment')
router.register(r'tasks', TaskViewSet, basename='task')
router.register(r'documents',DocumentViewset,basename='document')
#router.register(r'task',TaskViewSet,basename='task')
urlpatterns = [
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('register/', UserRegistrationView.as_view(), name='user_register'),
    path('profile/', UserProfileView.as_view(), name='user_profile'),
    path('users/', UserListView.as_view(), name='user_list'),
]