from django.shortcuts import get_object_or_404
from django.http import Http404
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from rest_framework import authentication, permissions
from .serializers import RestaurantInputSerializer, RestaurantOutputSerializer
from .models import Restaurant, Category
from .permissions import IsSuperAdmin

class RestaurantCreateApiView(APIView):

    permission_classes = [permissions.IsAuthenticated,IsSuperAdmin]
    
    def post(self,request):
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
        serializer = RestaurantInputSerializer(data = request.data)
        if serializer.is_valid():
            new_restaurant = serializer.save(restaurant_category = restaurant_category)
            output_serializer = RestaurantOutputSerializer(new_restaurant)
            print(output_serializer.data)
            return Response(output_serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)  