from django.shortcuts import get_object_or_404
from django.http import Http404
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from rest_framework import authentication, permissions
from .serializers import InventoryOutputSerializer
from restaurant.models import Restaurant, Category, Inventory
from restaurant.permissions import IsSuperAdmin


class InventoryApiView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        restaurant_id = request.user.restaurant

        try:
            restaurant = get_object_or_404(Restaurant, id=restaurant_id.id)
        except Http404:
            return Response(
                {"message": "restaurant not found"},
                status=status.HTTP_404_NOT_FOUND,
            )
        try:
            inventory = get_object_or_404(Inventory, restaurant=restaurant_id.id)
        except Http404:
            return Response(
                {"message": "inventory not found"},
                status=status.HTTP_404_NOT_FOUND,
            )
        restaurant_output_serializer = InventoryOutputSerializer(
            inventory, context={"request": request}
        )
        response_data = {
            "status": status.HTTP_200_OK,
            "error": False,
            "detail": restaurant_output_serializer.data,
            "message": "",
        }
        return Response(response_data)
