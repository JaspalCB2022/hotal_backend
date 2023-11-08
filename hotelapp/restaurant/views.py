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


class RestaurantCreateApiView(APIView):
    """
    API view for updating a restaurant's details.

    This view allows authenticated users with super admin permissions to create a restaurant.
    ```
    {
        "name": "Restaurant 1",
        "description": "Restaurant description 1",
        "opening_time": "10:30",
        "closing_time": "23:10",
        "phone_number": "9696997890",
        "address": "restaurant one address",
        "restaurant_category_id": "1"
    }
    ```
    """

    permission_classes = [permissions.IsAuthenticated, IsSuperAdmin]

    @extend_schema(request=None, responses=RestaurantInputSerializer)
    def post(self, request):
        restaurant_category_id = request.data.get("restaurant_category_id")
        if not restaurant_category_id:
            return Response(
                {"message": "restaurant category is required"},
                status=status.HTTP_404_NOT_FOUND,
            )
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
            new_restaurant_output_serializer = RestaurantOutputSerializer(
                new_restaurant
            )
            response_data = {
                "status": status.HTTP_201_CREATED,
                "error": False,
                "detail": new_restaurant_output_serializer.data,
                "message": "",
            }
            return Response(response_data)


class RestaurantUpdateApiView(APIView):
    """
    API view for updating a restaurant's details.

    This view allows authenticated users with super admin permissions to update the details of a restaurant.
    ```
    {
        "name":"restaurant_name",
        "description":"Restaurant description 1",
        "opening_time":"1:30",
        "closing_time":"16:10",
        "phone_number":"9898989898",
        "address":"restaurant one address"
    }
    ```
    """

    permission_classes = [permissions.IsAuthenticated, IsSuperAdmin]

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
            updatd_restaurant_serializer = RestaurantOutputSerializer(updatd_restaurant)
            response_data = {
                "status": status.HTTP_200_OK,
                "error": False,
                "detail": updatd_restaurant_serializer.data,
                "message": "",
            }
            return Response(response_data)


class RestaurantDeleteApiView(APIView):
    """
    API view for deleting a restaurants.
    This view allows authenticated users with super admin permissions to delete a restaurants.
    """

    permission_classes = [permissions.IsAuthenticated, IsSuperAdmin]

    def delete(self, request, restaurant_id, format=None):
        try:
            restaurant = Restaurant.objects.get(pk=restaurant_id)
        except Restaurant.DoesNotExist:
            response_data = {
                "status": status.HTTP_404_NOT_FOUND,
                "error": True,
                "detail": {},
                "message": "Restaurant not found",
            }
            return Response(response_data)

        restaurant.delete()
        return Response(
            {
                "status": status.HTTP_200_OK,
                "error": False,
                "detail": {},
                "message": "Restaurant Deleted Successfully",
            }
        )


class RestaurantListApiView(APIView):
    """
    API view for retrieving a list of restaurants.
    This view allows authenticated users with super admin permissions to retrieve a list of restaurants.
    """

    permission_classes = [permissions.IsAuthenticated, IsSuperAdmin]

    def get(self, request):
        restaurants = Restaurant.objects.all()
        restaurant_serializer = RestaurantOutputSerializer(restaurants, many=True)
        response_data = {
            "status": status.HTTP_200_OK,
            "error": False,
            "detail": restaurant_serializer.data,
            "message": "",
        }
        return Response(response_data)
