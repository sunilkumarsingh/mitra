# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.http import HttpResponse,JsonResponse
from django.contrib.auth.models import User
from rest_framework import viewsets, generics
from users.serializers import UserSerializer, UserTypeSerializer, EPC_DetailsSerializer, ProjectSerializer, ResetPasswordSerializer, \
    ConsumerRegisterSerializer,ModifyUserPasswordSerializer,CreateUserSerializer

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
from django.contrib.auth.hashers import make_password
import datetime

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


class ConsumerList(generics.ListCreateAPIView):
    """List of consumer users """


    model = User
    serializer_class = UserSerializer

    def get(self, request, *args, **kwargs):
        consumer_data = User.objects.filter(user_type__name="consumer", is_active=1).values()
        return HttpResponse(consumer_data, content_type="text/plain")


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


class ConsumerProjectList(generics.ListCreateAPIView):
    """ List of Projects of particular consumer"""

    model = Project_Details
    serializer_class = ProjectSerializer

    def get(self, request, *args, **kwargs):
        user_id = self.kwargs['id']
        project_data = Project_Details.objects.filter(consumer=user_id).values()
        return HttpResponse(project_data, content_type="text/plain")

class ProjectDetails(generics.ListCreateAPIView):
    """ View Project details """

    model = Project_Details
    serializer_class = ProjectSerializer

    def get(self, request, *args, **kwargs):
        project_id = self.kwargs['id']
        project_details= Project_Details.objects.filter(id=project_id).values()
        return HttpResponse(project_details, content_type="text/plain")


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
    serializer_class = ConsumerRegisterSerializer


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


class ProjectPaymentDetails(generics.ListCreateAPIView):
    """
    View Project payment details
    """
    def get(self,request, *args, **kwargs):
        project_id = self.kwargs["id"]
        payment_details= Payment_Details.objects.filter(project=project_id).values()
        return HttpResponse(payment_details)


class CreateUser(generics.ListCreateAPIView):
    """
    Create user 'EPC or  Investor or IPP' by admin
    """
    model = User
    queryset = User.objects.all()
    serializer_class = CreateUserSerializer

    def create(self, request, *args, **kwargs):
        request_data = request.POST.copy()
        request_data['password'] = make_password(request.data['password'])
        request_data['is_superuser'] = 0
        request_data['username'] = request.data['email']
        request_data["first_name"] = request.data.get('first_name', "")
        request_data["last_name"] = request.data.get('last_name', "")
        request_data['email'] = request.data['email']
        request_data['is_staff'] = 0
        request_data['is_active'] = 1
        request_data['date_joined'] = datetime.datetime.utcnow()
        request_data['user_type'] = request.data['user_type']
        serializer = self.get_serializer(data=request_data)
        if serializer.is_valid(raise_exception=True):
            auth_user = serializer.save()
            return Response(auth_user.id)
        else:
            return HttpResponse(serializer.errors, status=400)