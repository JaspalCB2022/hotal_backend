import os
from datetime import timedelta, datetime
from django.shortcuts import get_object_or_404, get_list_or_404
from django.http import Http404
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from rest_framework import authentication, permissions
from drf_spectacular.utils import extend_schema
from .serializers import RestaurantInputSerializer, RestaurantOutputSerializer, TableInputSerializer, TableOutputSerializer
from .models import Restaurant, Category, Table
from .permissions import IsSuperAdmin, IsRestaurant, IsSuperadminOrRestaurantOwner
from account.serializers import UserRegisterSerializer
from django.contrib.auth import get_user_model
from django.db import transaction
from io import BytesIO
from django.core.files.base import ContentFile


User = get_user_model()

# views.py
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Table
import qrcode
from django.db.models import Q
from django.core.serializers import serialize

class TableQRList(APIView):
    
    """
    API view for retrieving a list of restaurants.
    This view allows authenticated users with super admin permissions to retrieve a list of restaurants.
    """

    permission_classes = [permissions.IsAuthenticated, IsSuperadminOrRestaurantOwner]

    def get(self, request):
        try:
            restaurant_id = request.user.restaurant.id
            tables_with_qr = Table.objects.filter(Q(restaurant=restaurant_id) & Q(qrlink__isnull=False) & Q(is_active=True))
            json_data_list = TableOutputSerializer(tables_with_qr, many=True ,context={'request': request})
            response_data = {
                "status": status.HTTP_200_OK,
                "error": False,
                "detail": json_data_list.data,
                "message": "",
            }
            return Response(response_data)
        except AttributeError:
            response_data = {
                "status": status.HTTP_400_BAD_REQUEST,
                "error": True,
                "detail": [],
                "message": "User does not have an associated restaurant.",
            }
            return Response(response_data)
class TableQRCodeView(APIView):
    def get(self, request, table_id):
        try:
            table = Table.objects.get(id=table_id)
        except Table.DoesNotExist:
            return Response({"error": "Table not found"}, status=404)
        if table.qrlink is not None and table.is_active is not False:
            return Response({"message": f"Table Number {table.tablenumber} QR Code already exists.", 'detail': [], 'error': False, "status":status.HTTP_403_FORBIDDEN})
        else:
            serializer = TableOutputSerializer(table, many=False, context={"request": request})
            serialized_data = serializer.data
            qr = qrcode.QRCode(
                version=1,
                error_correction=qrcode.constants.ERROR_CORRECT_L,
                box_size=10,
                border=4,
            )
            qr.add_data(str(serialized_data))  # Use the table's ID for the QR code
            qr.make(fit=True)
            qr_img = qr.make_image(fill_color="black", back_color="white")
            img_io = BytesIO()
            qr_img.save(img_io, format='PNG')
            
            filename = f"table_{table.id}_qr.png"
            qrimglink = ContentFile(img_io.getvalue(), name=filename)
            table.qrlink = qrimglink
            table.is_active = True
            table.save()
            return Response({"message": f"Table Number {table.tablenumber} QR Code created successfully", 'detail': [], 'error': False, "status":status.HTTP_201_CREATED})
        


class TableListApiView(APIView):
    """
    API view for retrieving a list of restaurants.
    This view allows authenticated users with super admin permissions to retrieve a list of restaurants.
    """

    permission_classes = [permissions.IsAuthenticated, IsSuperadminOrRestaurantOwner]

    def get(self, request):
        restaurantid = request.user.restaurant.id
        tables = Table.objects.filter(restaurant = restaurantid)
        restaurant_serializer = TableInputSerializer(
            tables, many=True, context={"request": request}
        )
        response_data = {
            "status": status.HTTP_200_OK,
            "error": False,
            "detail": restaurant_serializer.data,
            "message": "",
        }
        return Response(response_data)
class TableCreateApiView(APIView):
    """
    API view for updating a restaurant's details.

    This view allows authenticated users with super admin, or restaurant owner  permissions to create a Table.
    ```
    {
        "table_number": 3,
        "capacity": 5,
        "is_occupied" : false
    }

    ```
    """

    permission_classes = [permissions.IsAuthenticated, IsSuperadminOrRestaurantOwner]

    @extend_schema(request=None, responses=TableInputSerializer)
    @transaction.atomic
    def post(self, request):
        #print("request.data >>>", request.data)
        tablenumber = request.data.get("tablenumber")
        capacity = request.data.get("capacity")
        is_occupied = request.data.get("is_occupied")
        restaurant = request.user.restaurant
        #print("restaurant >>>", restaurant)
        serializer = TableInputSerializer(data=request.data)
        
        if serializer.is_valid(raise_exception=True):
            #serializer.save()
            new_inventory = serializer.save(
                tablenumber=int(tablenumber),
                capacity=int(capacity),
                is_occupied= True if is_occupied.lower() =='true' else False,
                restaurant=restaurant,
            )
            new_inventory.save()
            return Response({'message': 'table created successfully.', 'detail': [], 'error': False, 'status': status.HTTP_200_OK}, status=status.HTTP_200_OK)
        else:
            return Response(
                {"message": "Validation Error", 'detail': serializer.errors, 'error': True, 'status': status.HTTP_400_BAD_REQUEST},
                status=status.HTTP_400_BAD_REQUEST
            )
   

class RestaurantCreateApiView(APIView):
    """
    API view for updating a restaurant's details.

    This view allows authenticated users with super admin permissions to create a restaurant.
    ```
    {
        "name": "restaurant 28888",
        "email": "restaurnat8@email.com",
        "description": "test description",
        "opening_time": "10:30",
        "closing_time": "23:10",
        "phone_number": "7777777777",
        "address": "test address",
        "restaurant_category_id": 1,
        "is_open_on_sunday": true,
        "is_open_on_monday": true,
        "is_open_on_tuesday": true,
        "is_open_on_wednesday": false,
        "is_open_on_thursday": false,
        "is_open_on_friday": false,
        "is_open_on_saturday": false
        "logo":<image>
    }

    ```
    """

    permission_classes = [permissions.IsAuthenticated, IsSuperAdmin]

    @extend_schema(request=None, responses=RestaurantInputSerializer)
    @transaction.atomic
    def post(self, request):
        restaurant_category_id = request.data.get("restaurant_category_id")
        email = request.data.get("email")

        if not restaurant_category_id:
            return Response(
                {"message": "restaurant category is required"},
                status=status.HTTP_404_NOT_FOUND,
            )
        try:
            restaurant = get_object_or_404(Restaurant, email=email)
            user = get_object_or_404(User, email=email)
            if restaurant or user:
                return Response(
                    {"message": "Restaurant with this email already exists."},
                    status=status.HTTP_404_NOT_FOUND,
                )
        except Http404:
            pass
        try:
            restaurant_category = get_object_or_404(Category, id=restaurant_category_id)
        except Http404:
            return Response(
                {"message": "restaurant category not found"},
                status=status.HTTP_404_NOT_FOUND,
            )
        serializer = RestaurantInputSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            new_restaurant = serializer.save(restaurant_category=restaurant_category)
            user = User.objects.create(
                email=request.data.get("email"),
                first_name=request.data.get("name"),
                role="restaurant",
                restaurant=new_restaurant,
            )
            user.save()
            new_restaurant_output_serializer = RestaurantOutputSerializer(
                new_restaurant, context={"request": request}
            )
            response_data = {
                "status": status.HTTP_201_CREATED,
                "error": False,
                "detail": new_restaurant_output_serializer.data,
                "message": "",
            }
            return Response(response_data, status=status.HTTP_201_CREATED)


class RestaurantUpdateApiView(APIView):
    """
    API view for updating a restaurant's details.

    This view allows authenticated users with super admin permissions to update the details of a restaurant.
    ```
    {
        "name": "restaurant 28888",
        "email": "restaurnat8@email.com",
        "description": "test description",
        "opening_time": "10:30",
        "closing_time": "23:10",
        "phone_number": "7777777777",
        "address": "test address",
        "restaurant_category_id": 1,
        "is_open_on_sunday": true,
        "is_open_on_monday": true,
        "is_open_on_tuesday": true,
        "is_open_on_wednesday": false,
        "is_open_on_thursday": false,
        "is_open_on_friday": false,
        "is_open_on_saturday": false
        "logo":<image>
    }
    ```
    """

    permission_classes = [permissions.IsAuthenticated, IsSuperadminOrRestaurantOwner]

    @transaction.atomic
    def put(self, request, restaurant_id):
        try:
            restaurant = Restaurant.objects.get(id=restaurant_id)
        except Restaurant.DoesNotExist:
            return Response(
                {"error": "Restaurant not found"}, status=status.HTTP_404_NOT_FOUND
            )
        serializer = RestaurantInputSerializer(restaurant, data=request.data)
        if serializer.is_valid(raise_exception=True):
            updatd_restaurant = serializer.save()
            #print("updatd_restaurant >>>", updatd_restaurant)
            # user = User.objects.get(restaurant=updatd_restaurant)
            # user.first_name = updatd_restaurant.name
            # user.email = updatd_restaurant.email
            # user.save()
            updatd_restaurant_serializer = RestaurantOutputSerializer(
                updatd_restaurant, context={"request": request}
            )
            response_data = {
                "status": status.HTTP_200_OK,
                "error": False,
                "detail": updatd_restaurant_serializer.data,
                "message": "",
            }
            return Response(response_data, status=status.HTTP_200_OK)


class RestaurantDeleteApiView(APIView):
    """
    API view for deleting a restaurants.
    This view allows authenticated users with super admin permissions to delete a restaurants.
    """

    permission_classes = [permissions.IsAuthenticated, IsSuperAdmin]

    def delete(self, request, restaurant_id):
        try:
            restaurant = Restaurant.objects.get(pk=restaurant_id)
        except Restaurant.DoesNotExist:
            response_data = {
                "status": status.HTTP_404_NOT_FOUND,
                "error": True,
                "detail": {},
                "message": "Restaurant not found",
            }
            return Response(response_data, status=status.HTTP_404_NOT_FOUND)

        restaurant.delete()
        return Response(
            {
                "status": status.HTTP_200_OK,
                "error": False,
                "detail": {},
                "message": "Restaurant Deleted Successfully",
            },
            status=status.HTTP_200_OK,
        )


class RestaurantListApiView(APIView):
    """
    API view for retrieving a list of restaurants.
    This view allows authenticated users with super admin permissions to retrieve a list of restaurants.
    """

    permission_classes = [permissions.IsAuthenticated, IsSuperAdmin]

    def get(self, request):
        restaurants = Restaurant.objects.all()
        restaurant_serializer = RestaurantOutputSerializer(
            restaurants, many=True, context={"request": request}
        )
        response_data = {
            "status": status.HTTP_200_OK,
            "error": False,
            "detail": restaurant_serializer.data,
            "message": "",
        }
        return Response(response_data, status=status.HTTP_200_OK)


class RestaurantDetailApiView(APIView):

    """
    Api view to get detail of restaurant by id.
    """

    permission_classes = [permissions.IsAuthenticated, IsSuperAdmin]

    def get(self, request, restaurant_id):
        try:
            restaurant = get_object_or_404(Restaurant, id=restaurant_id)
        except Http404:
            return Response(
                {"message": "restaurant not found"},
                status=status.HTTP_404_NOT_FOUND,
            )
        restaurant_output_serializer = RestaurantOutputSerializer(
            restaurant, context={"request": request}
        )
        response_data = {
            "status": status.HTTP_200_OK,
            "error": False,
            "detail": restaurant_output_serializer.data,
            "message": "",
        }
        return Response(response_data, status=status.HTTP_200_OK)


class RestaurantUpdateOwnProfile(APIView):
    """
    Api for restaurnt to update their profile.
    """

    permission_classes = [permissions.IsAuthenticated]

    @transaction.atomic
    def put(self, request):
        restaurant = request.user.restaurant
        del request.data["email"]
        try:
            restaurant = Restaurant.objects.get(pk=restaurant.id)
        except Restaurant.DoesNotExist:
            return Response(
                {"error": "Restaurant not found"}, status=status.HTTP_404_NOT_FOUND
            )
        serializer = RestaurantInputSerializer(restaurant, data=request.data)
        if serializer.is_valid(raise_exception=True):
            updatd_restaurant = serializer.save()
            user = User.objects.get(restaurant=updatd_restaurant)
            user.first_name = updatd_restaurant.name
            user.email = updatd_restaurant.email
            user.save()
            updatd_restaurant_serializer = RestaurantOutputSerializer(
                updatd_restaurant, context={"request": request}
            )
            response_data = {
                "status": status.HTTP_200_OK,
                "error": False,
                "detail": updatd_restaurant_serializer.data,
                "message": "",
            }
            return Response(response_data, status=status.HTTP_200_OK)

        response_data = {
            "status": status.HTTP_200_OK,
            "error": False,
            "detail": "",
            "message": "",
        }
        return Response(response_data, status=status.HTTP_200_OK)
