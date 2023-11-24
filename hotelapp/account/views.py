from django.shortcuts import get_object_or_404, render
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
    KicthenStaffUpdateSerializer,
    UserSerializer,
    UserRegisterSerializer,
    PasswordResetSerializer,
    ForgotPasswordSerializer,
    KitchenStaffChangePasswordSerializer
    # ChangePasswordSerializer,
)
from drf_spectacular.utils import extend_schema
from django.db import IntegrityError
from django.http import Http404
from django.template.loader import render_to_string
from django.contrib.sites.shortcuts import get_current_site
from .permissions import IsSuperAdmin, IsSuperadminOrRestaurantOwner
from .utils import send_email_message
from rest_framework.permissions import IsAuthenticated
from django.db.models import Q
from django.contrib.auth import get_user_model


class KitchenStaffDeleteAPIView(APIView):
    permission_classes = [IsAuthenticated, IsSuperadminOrRestaurantOwner]

    def delete(self, request, pk, format=None):
        try:
            user = User.objects.get(id=pk)
            if user.role is 'kitchen_staff':
                user.delete()
                return Response({
                    "status": status.HTTP_204_NO_CONTENT,
                    "error": False,
                    "detail": [],
                    "message": "User delete Successfully.",
                    },status=status.HTTP_204_NO_CONTENT)
            else:
                return Response({
                    "status": status.HTTP_404_NOT_FOUND,
                    "error": False,
                    "detail": [],
                    "message": "Kitchen Staff User not Found.",
                    },status=status.HTTP_204_NO_CONTENT)
        except User.DoesNotExist:
            return Response({
                "status": status.HTTP_404_NOT_FOUND,
                "error": True,
                "detail": [],
                "message": "User does not exist",
            },status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'error': f'An error occurred: {str(e)}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class KitcheStaffChangePasswordAPIView(APIView):
    permission_classes = [IsAuthenticated, IsSuperadminOrRestaurantOwner]
    @extend_schema(request=None, responses=KitchenStaffChangePasswordSerializer)
    def post(self, request):
        serializer = KitchenStaffChangePasswordSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data['email']
            try:
                user = get_user_model().objects.get(email=email)
            except get_user_model().DoesNotExist:
                return Response({
                "status": status.HTTP_404_NOT_FOUND,
                "error": True,
                "detail": "",
                "message": 'User not found',
            }, status=status.HTTP_404_NOT_FOUND)

            serializer.update_password(user, serializer.validated_data)
            response_data = {
                "status": status.HTTP_200_OK,
                "error": False,
                "detail": "",
                "message": 'Password changed successfully',
            }
            return Response(response_data, status=status.HTTP_200_OK)
        return Response({
                "status": status.HTTP_400_BAD_REQUEST,
                "error": True,
                "detail": serializer.errors,
                "message": 'Validation Error!',
            } , status=status.HTTP_400_BAD_REQUEST)

class UpdateKitcheStaffUserApiView(APIView):
    permission_classes = [IsAuthenticated, IsSuperadminOrRestaurantOwner]
    @extend_schema(request=None, responses=KicthenStaffUpdateSerializer)
    def put(self, request, userid,*args, **kwargs):
        restaurant = getattr(request.user, 'restaurant', None)
        # Check if the current user has a restaurant
        if not restaurant:
            response_data = {
                "status": status.HTTP_401_UNAUTHORIZED,
                "error": False,
                "detail": "",
                "message": "Your user account does not have a associated restaurant.",
            }
            return Response(response_data, status=status.HTTP_401_UNAUTHORIZED)

        checkUser = get_object_or_404(User, id=userid)

        # Check if the checkUser has a restaurant
        if not checkUser.restaurant:
            response_data = {
                "status": status.HTTP_404_NOT_FOUND,
                "error": False,
                "detail": "",
                "message": "The specified user does not have an associated restaurant.",
            }
            return Response(response_data, status=status.HTTP_404_NOT_FOUND)

        # Check if the current user's restaurant is not equal to the checkUser's restaurant
        if restaurant.id != checkUser.restaurant.id:
            response_data = {
                "status": status.HTTP_401_UNAUTHORIZED,
                "error": False,
                "detail": "",
                "message": "You are not authorized to perform this action.",
            }
            return Response(response_data, status=status.HTTP_401_UNAUTHORIZED)
        else:
            #staff_instance = get_user_model().objects.get(pk=userid)  # Retrieve the instance by its primary key
            serializer = KicthenStaffUpdateSerializer(checkUser, data=request.data)
            if serializer.is_valid():
                serializer.save()  # This will call the update method in your serializer
                response_data = {
                    "status": status.HTTP_200_OK,
                    "error": False,
                    "detail": "",
                    "message": "User data updated successfully.",
                }
            # return Response(response_data, status=status.HTTP_200_OK)
                return Response(response_data, status=status.HTTP_200_OK)
            return Response({'status':status.HTTP_400_BAD_REQUEST,'message':'validation Error!', 'detail': serializer.errors, 'error':True} )
               
            


class GetAllKitchenUserApiView(APIView):
    """
    Api view for listing users
    This view retrieves a list of All Active and In-Active Kitchen Staff Users.
    It is restricted to superadmin or restaurant owner users only.
    """
    permission_classes = [IsAuthenticated, IsSuperadminOrRestaurantOwner]
    serializer_class = UserSerializer
    def get(self, request):
        """
        Return a list of All Active and In-Active Kitchen Staff Users.
        """ 
        isactive=request.query_params.get("isactive")
        #print("isactive >>>>", isactive)
        try:
            if isactive and isactive.lower() =='true':
                userObj = User.objects.filter(Q(role="kitchen_staff") & Q(is_active = True) & Q(is_staff=True) )
                user = UserSerializer(userObj, many=True ,context={'request':request}).data
                resObj = {'status':status.HTTP_200_OK,'message':'', 'detail':user, 'error':False}
            elif  isactive and isactive.lower() =='false':
                userObj = User.objects.filter(Q(role="kitchen_staff") & Q(is_active = False) & Q(is_staff=True) )
                user = UserSerializer(userObj, many=True ,context={'request':request}).data
                resObj = {'status':status.HTTP_200_OK,'message':'', 'detail':user, 'error':False}
            else:
                resObj = {'status':status.HTTP_400_BAD_REQUEST,'message':'', 'detail':[], 'error':True}

            return Response(resObj, status=status.HTTP_200_OK)
            
        except User.DoesNotExist:
            resObj = {'status':status.HTTP_200_OK,'message':'Kitchen Staff users does not exists.', 'detail':[], 'error':False}
            return Response(resObj, status=status.HTTP_200_OK)



class CreateKitchenUserAPIView(APIView):
    permission_classes = [IsAuthenticated, IsSuperadminOrRestaurantOwner]
    @extend_schema(request=None, responses=UserRegisterSerializer)
    def post(self, request, *args, **kwargs):
        first_name = request.data.get('first_name')
        last_name = request.data.get('last_name')
        email = request.data.get('email')
        password = request.data.get('password')
        is_active =  request.data.get('is_active')
        role = 'kitchen_staff'
        serializer = UserRegisterSerializer(data=request.data)
        if serializer.is_valid():
            new_serializer = serializer.save(
                first_name= first_name,
                last_name= last_name,
                email= email,
                password= password,
                role= role,
                is_active =  True if is_active.lower() == 'ture' else False,
                is_staff =  True,
                restaurant= request.user.restaurant
            )
            new_serializer.save()
            return Response({'status':status.HTTP_201_CREATED,'message':'user created successfully.', 'detail': [], 'error':False} , status=status.HTTP_201_CREATED)
        
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



