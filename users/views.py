# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.http import HttpResponse,JsonResponse

from django.contrib.auth.models import User
from rest_framework import viewsets, generics
from rest_framework.response import Response
from users.serializers import UserSerializer, UserTypeSerializer, EPC_DetailsSerializer, ProjectSerializer, ResetPasswordSerializer, UserRegisterSerializer,ModifyUserPasswordSerializer

from django.views.generic.base import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from models import *
from rest_framework.generics import CreateAPIView
from django.contrib.auth import authenticate
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.status import HTTP_401_UNAUTHORIZED
from rest_framework.authtoken.models import Token
from django.contrib.auth import get_user_model
from rest_framework import permissions

class PowerMitraIndex(TemplateView):
    template_name = "client/index.html"

# @login_required(login_url="login/")
class PowerMitraAdmin(LoginRequiredMixin, TemplateView):
    """
        Home page for PM Admin portal
    """
    template_name = "backend/index.html"
    login_url = '/login/'

class UsersViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer

class UserLogin(generics.ListCreateAPIView):
    """
    Users Login api
    """
    def post(self, request, *args, **kwargs):
        email = request.data['email']
        password = request.data['password']
        user = authenticate(username=email, password=password)
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


class UsersList(generics.ListCreateAPIView):
    """List the users"""
    model = User
    serializer_class = UserSerializer
    queryset = User.objects.filter(is_active=1)


class EPCList(generics.ListCreateAPIView):
    """List of EPC users """

    model = EPC_Details
    queryset= EPC_Details.objects.filter(user_id__user_type__name="epc", user_id__is_active=1)
    serializer_class = EPC_DetailsSerializer


class InvestorList(generics.ListCreateAPIView):
    """List of Investor users """

    model = User
    serializer_class = UserSerializer

    def get(self, request, *args, **kwargs):
        investor_data = User.objects.filter(user_type__name="investor", is_active=1).values()
        return HttpResponse(investor_data, content_type="text/plain")


class UserTypeList(generics.ListCreateAPIView):
    """ List of user types"""

    model = UserType
    serializer_class = UserTypeSerializer

    def get(self, request, *args, **kwargs):
        usertype_list = UserType.objects.all().values()
        return HttpResponse(usertype_list, content_type="text/plain")


class ProjectList(generics.ListCreateAPIView):
    """ List of Projects of particular consumer"""

    model = Project_Details
    serializer_class = ProjectSerializer

    def get(self, request, *args, **kwargs):
        user_id = self.kwargs['id']
        project_data = Project_Details.objects.filter(consumer=user_id).values()
        return HttpResponse(project_data, content_type="text/plain")


class UpdateUserStatus(generics.RetrieveUpdateAPIView):
    """
    Update user status fron active to inactive
    """
    model = User
    queryset = User.objects.all()
    serializer_class = UserSerializer
    lookup_field = 'id'

    def perform_update(self, serializer):
        instance = self.get_object()
        modified_instance = serializer.save(is_active=0)
        return modified_instance


class UserPasswordReset(generics.GenericAPIView):
    """
    Reset password of the current user.
    """
    serializer_class = ResetPasswordSerializer

    def post(self, request, format=None):
        serializer_class = self.get_serializer_class()
        serializer = serializer_class(data=request.data, instance=request.user)
        if serializer.is_valid():
            serializer.save()
            return Response({'message': (u'Password successfully changed')})
        return Response(serializer.errors, status=400)


class ModifyUserPassword(generics.GenericAPIView):
    """
    Modify user password by admin
    """
    serializer_class = ModifyUserPasswordSerializer

    def post(self, request, format=None):
        user_id = request.data['user_id']
        # user_id=6
        try:
            serializer_class = self.get_serializer_class()
            serializer = serializer_class(data=request.data, instance = user_id)
            if serializer.is_valid():
                serializer.save()
                return Response({'message': (u'Password successfully changed')})

            return Response(serializer.errors, status=400)
        except Exception as e:
            return Response(str(e.message), status=400)


class RegisterUserView(CreateAPIView):
    """Register user with email, mobile no, password """

    model = get_user_model()
    permission_classes = [
        permissions.AllowAny
    ]
    serializer_class = UserRegisterSerializer


class ConsumerEPCList(generics.CreateAPIView):
    """
    List consumers EPC list
    """
    def get(self,request, *args, **kwargs):
        project_id = self.kwargs["id"]
        project_epc = Project_Details.objects.filter(id=project_id).values()
        return HttpResponse(project_epc)

class ConsumerWithEPCReview(generics.CreateAPIView):
    """
    Create Consumer with Epc Review
    """
    model = Project_Details
    queryset = Project_Details.objects.all()
    serializer_class = ProjectSerializer

    def post(self, request, *args, **kwargs):
        loggedinuser = request.data['consumer']
        selected_epc = request.data["epc"]
        epcreview = request.data["epc_review"]
        try:
            updated, created = Project_Details.objects.update_or_create(
                epc=selected_epc,
                consumer=loggedinuser,
                defaults={
                    "epc_review": epcreview
                }
            )
            return JsonResponse({"message": 'Updated Review'})
        except Exception as e:
            return HttpResponse(e, status=500)


