from .models import *
from rest_framework import serializers
from django.contrib.auth.models import User

class UserSerializer(serializers.ModelSerializer):
    class meta :
        model = User
        fields = ('id','username','email','first_name','last_name')

class UserProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    class meta:
        model = UserProfile
        fields = ('id', 'user', 'phone_number', 'address', 'role', 'created_at', 'updated_at')
        read_only_fields = ('created_at', 'updated_at')


class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    profile = UserProfileSerializer(required=False)
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'password', 'first_name', 'last_name', 'profile')
    
    def create(self,validated_data):
        profile_data = validated_data.pop('profile',{})
        user = User.objects.create_user(**validated_data)
        UserProfile.objects.create(user=user,**profile_data)
        return user

class ContactSerializer(serializers.ModelSerialzer):
    class Meta:
        model = Contact
        fields = '__all__'
        read_only_fields = ('created_at','updated_at','user')

        def create(self,validated_data):
            #set user to currently authenticated user
            validated_data['user'] = self.context['request'].user
            return super().create(validated_data)

class PropertySerializer(serializers.ModelSerializer):
    class Meta:
        model = Property
        fields = '__all__'
        read_only_fields = ('created_at','updated_at','user')
    
    def create(self,validated_data):
        validated_data['user'] = self.context['request'].user
        return super().create(validated_data)