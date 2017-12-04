from django.contrib.auth.models import User, Group
from rest_framework import serializers
from models import User, UserType


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'email','id','is_active') #('__all__')


class UserTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserType
        fields = ('__all__')