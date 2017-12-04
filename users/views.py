# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.http import HttpResponse

from django.contrib.auth.models import User
from rest_framework import viewsets, generics
from rest_framework.response import Response
from users.serializers import UserSerializer, UserTypeSerializer

from django.views.generic.base import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from models import User, UserType

from django.contrib.auth import authenticate
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.status import HTTP_401_UNAUTHORIZED
from rest_framework.authtoken.models import Token

class PowerMitraIndex(TemplateView):
    template_name = "index.html"
    
class UsersViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer

class UserLogin(generics.ListCreateAPIView):
    def post(self, request, *args, **kwargs):
        email = request.data['email']
        password = request.data['password']
        user = authenticate(email=email, password=password)
        if not user:
            return Response({
                    "status": "failed",
                    "message": "Please enter a correct username and password."
                    }, status=HTTP_401_UNAUTHORIZED)

        # return Response({"status":'success',"id": user.id,"email": user.email,'name':user.username})
        if user.is_active:
            serialized = UserSerializer(user)
            return Response({
                "status": "success",
                "data":serialized.data})
        else:
            return Response({
                'status': "failed",
                'message': "Your account is not active, Please contact to administrator."
                }, status=HTTP_401_UNAUTHORIZED)


class LoggedUserList(generics.ListCreateAPIView):
    model = User
    serializer_class = UserSerializer

    def post(self, request, *args, **kwargs):
        print "call user list using post"
        email = request.data['email']
        password = request.data['password']

        queryset = User.objects.all()
        print queryset.query
        return  Response(UserSerializer(queryset, many=True).data)