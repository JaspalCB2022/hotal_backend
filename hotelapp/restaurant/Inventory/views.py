from django.shortcuts import get_object_or_404
from django.http import Http404
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from rest_framework import authentication, permissions
from .serializers import InventoryOutputSerializer, InventoryInputSerializer
from restaurant.models import (
    Restaurant,
    Category,
    Inventory,
    MenuTypes,
    Menu_Subtype,
    UnitCategory,
)
from restaurant.permissions import IsSuperAdmin, IsRestaurant


class InventoryListApiView(APIView):
    permission_classes = [permissions.IsAuthenticated, IsRestaurant]

    def get(self, request):
        restaurant_id = request.user.restaurant
        try:
            inventory = get_object_or_404(Inventory, restaurant=restaurant_id.id)
        except Http404:
            return Response(
                {"message": "inventory not found"},
                status=status.HTTP_404_NOT_FOUND,
            )
        inventory_output_serializer = InventoryOutputSerializer(
            inventory, context={"request": request}
        )
        response_data = {
            "status": status.HTTP_200_OK,
            "error": False,
            "detail": inventory_output_serializer.data,
            "message": "",
        }
        return Response(response_data)


class InventoryCreateApiView(APIView):
    permission_classes = [permissions.IsAuthenticated, IsRestaurant]

    def post(self, request):
        menu_type = request.data.get("menu_type")
        menu_subtype = request.data.get("menu_subtype")
        unit_category = request.data.get("unit_category")
        restaurant = request.user.restaurant

        if not menu_subtype or not menu_type or not unit_category:
            return Response(
                {"message": "Validation error"},
                status=status.HTTP_404_NOT_FOUND,
            )
        try:
            menu_type = get_object_or_404(MenuTypes, id=menu_type)
        except Http404:
            return Response(
                {"message": "menu type not found"},
                status=status.HTTP_404_NOT_FOUND,
            )
        try:
            menu_subtype = get_object_or_404(Menu_Subtype, id=menu_subtype)
        except Http404:
            return Response(
                {"message": "menu subtype not found"},
                status=status.HTTP_404_NOT_FOUND,
            )
        try:
            unit_category = get_object_or_404(UnitCategory, id=unit_category)
        except Http404:
            return Response(
                {"message": "unit not found"},
                status=status.HTTP_404_NOT_FOUND,
            )
        inventory_serializer = InventoryInputSerializer(data=request.data)
        if inventory_serializer.is_valid(raise_exception=True):
            new_inventory = inventory_serializer.save(
                menu_type=menu_type,
                menu_subtype=menu_subtype,
                unit_category=unit_category,
                restaurant=restaurant,
            )
            inventory_output_serializer = InventoryOutputSerializer(
                new_inventory, context={"request": request}
            )
        response_data = {
            "status": status.HTTP_200_OK,
            "error": False,
            "detail": inventory_output_serializer.data,
            "message": "",
        }
        return Response(response_data)


class InventoryDeleteApi(APIView):
    pass
