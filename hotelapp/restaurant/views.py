from django.shortcuts import get_object_or_404
from django.http import Http404
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from rest_framework import authentication, permissions
from drf_spectacular.utils import extend_schema
from .serializers import RestaurantInputSerializer, RestaurantOutputSerializer
from .models import Restaurant, Category
from .permissions import IsSuperAdmin
from account.serializers import UserRegisterSerializer
from django.contrib.auth import get_user_model
from django.db import transaction

User = get_user_model()


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

    permission_classes = [permissions.IsAuthenticated, IsSuperAdmin]

    @transaction.atomic
    def put(self, request, restaurant_id):
        try:
            restaurant = Restaurant.objects.get(pk=restaurant_id)
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
