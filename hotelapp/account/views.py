from django.shortcuts import render
import uuid
# Create your views here.
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from django.utils import timezone
from rest_framework.generics import (
    CreateAPIView,
    ListAPIView,
    RetrieveUpdateAPIView,
    DestroyAPIView,
    RetrieveAPIView,
    UpdateAPIView,
    RetrieveUpdateAPIView,
)
from django.contrib.auth import authenticate

#from .Password import setPasswordForUser
from .models import User
from .serializers import (
    UserSerializer,
    # UserRegisterSerializer,
    PasswordResetSerializer,
    ForgotPasswordSerializer,
    UserKictenStaffSerializer,
    # ChangePasswordSerializer,
)
from drf_spectacular.utils import extend_schema
from django.db import IntegrityError
from django.http import Http404
from django.template.loader import render_to_string
from django.contrib.sites.shortcuts import get_current_site
from .permissions import IsSuperAdmin
from .utils import send_email_message
from rest_framework.permissions import IsAuthenticated




class CreateUserAPIView(APIView):
    def post(self, request, *args, **kwargs):

        first_name = request.data.get('first_name')
        last_name = request.data.get('last_name')
        phone_number = request.data.get('phone_number')
        password = request.data.get('password')
        role = 'kitchen_staff'

        
        serializer = UserKictenStaffSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save({
                first_name,
                last_name,
                phone_number,
                
            })
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
        return Response({'status':status.HTTP_400_BAD_REQUEST,'message':'validation Error!', 'detail': serializer.errors, 'error':True} , status=status.HTTP_400_BAD_REQUEST)


class CurrentUserApiView(APIView):
    """
    Api view for listing users

    This view retrieves a list of users, excluding those with the "superadmin" role.
    It is restricted to superadmin users only.
    """
    permission_classes = [IsAuthenticated]
    serializer_class = UserSerializer

    def get(self, request, format=None):
        """
        Return a list of all users.
        """ 
        try:
            print("Request>>>", self.request)
            userObj = User.objects.get(email=self.request.user)
            user = UserSerializer(userObj, context={'request':request}).data
            
            resObj = {'status':status.HTTP_200_OK,'message':'', 'detail':user, 'error':False}
            return Response(resObj, status=status.HTTP_200_OK)
        except User.DoesNotExist:
            resObj = {'status':status.HTTP_200_OK,'message':'User does not exists.', 'detail':[], 'error':False}
            return Response(resObj, status=status.HTTP_200_OK)



class ResetPasswordAPIView(APIView):
    """
    API view for setting a user's password.

    This view provides endpoints for setting a user's password using a valid password reset token.
    """

    def get_user(self, token):
        try:
            uuid_token = uuid.UUID(token)
        except ValueError:
            return None
        try:
            user = User.objects.get(password_reset_token=token)
            if (timezone.now() - user.token_create_at).total_seconds() <= 300:
                return user
            else:
                return None
        except User.DoesNotExist:
            return None

    @extend_schema(request=None, responses=PasswordResetSerializer)
    def post(self, request, token):
        user = self.get_user(token)
        if user is None:
            return Response(
                {"message": "Invalid, expired, or used token"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        serializer = PasswordResetSerializer(data=request.data)
        serializer.is_valid()
        new_password = serializer.validated_data.get("password")
        user.set_password(new_password)
        user.password_reset_token = None
        user.token_create_at = None
        user.is_active = True
        user.save()
        return Response(
            {"message": "Password set successfully"},
            status=status.HTTP_200_OK,
        )
        # return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ResetPasswordAPIView(APIView):
    """
    API view for setting a user's password.

    This view provides endpoints for setting a user's password using a valid password reset token.
    """

    def get_user(self, token):
        try:
            uuid_token = uuid.UUID(token)
        except ValueError:
            return None
        try:
            user = User.objects.get(password_reset_token=token)
            if (timezone.now() - user.token_create_at).total_seconds() <= 300:
                return user
            else:
                return None
        except User.DoesNotExist:
            return None

    @extend_schema(request=None, responses=PasswordResetSerializer)
    def post(self, request, token):
        user = self.get_user(token)
        if user is None:
            return Response(
                {"message": "Invalid, expired, or used token"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        serializer = PasswordResetSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        new_password = serializer.validated_data.get("password")
        user.set_password(new_password)
        user.password_reset_token = None
        user.token_create_at = None
        user.is_active = True
        user.save()
        return Response(
            {"message": "Password set successfully"},
            status=status.HTTP_200_OK,
        )
        # return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ForgotPasswordApiView(APIView):
    """
    API view for handling password reset requests.
    """

    @extend_schema(request=None, responses=ForgotPasswordSerializer)
    def post(self, request):
        serializer = ForgotPasswordSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.validated_data["email"]
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return Response(
                {"message": "User with this email address does not exist."},
                status=status.HTTP_400_BAD_REQUEST,
            )
        token = user.generate_password_reset_token()
        subject = "password reset request."
        message = render_to_string(
            "email_templates/set_password_email.html",
            {
                "token": token,
                "user": user,
                "domain": get_current_site(self.request),
                "protocol": "http",
            },
        )
        send_email_message(user.email, subject, message)
        return Response(
            {"message": "Password reset link sent to your email."},
            status=status.HTTP_200_OK,
        )
        # return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



