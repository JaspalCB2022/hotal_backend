from django.shortcuts import get_object_or_404
from django.http import Http404
from rest_framework.parsers import MultiPartParser, FormParser
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
        menu_type = request.query_params.get("menu_type")
        subtype = request.query_params.get("subtype")

        filters = {"restaurant": restaurant_id.id}

        if menu_type:
            filters["menu_type__name"] = menu_type

        if subtype:
            filters["menu_subtype__name"] = subtype

        inventory = Inventory.objects.filter(**filters)

        if not inventory.exists():
            return Response(
                {"message": "Inventory not found"},
                status=status.HTTP_404_NOT_FOUND,
            )
        inventory_output_serializer = InventoryOutputSerializer(
            inventory, context={"request": request}, many=True
        )
        response_data = {
            "status": status.HTTP_200_OK,
            "error": False,
            "detail": inventory_output_serializer.data,
            "message": "",
        }
        return Response(response_data, status=status.HTTP_200_OK)


class InventoryCreateApiView(APIView):
    permission_classes = [permissions.IsAuthenticated, IsRestaurant]
    parser_classes = (MultiPartParser, FormParser)

    def post(self, request, *args, **kwargs):
        json_data = request.data.get("json_data", {})
        image_file = request.data.get("image")

        # Validate and save JSON data
        inventory_serializer = InventoryInputSerializer(data=json_data)
        if inventory_serializer.is_valid():
            menu_type = get_object_or_404(MenuTypes, id=json_data.get("menu_type"))
            menu_subtype = get_object_or_404(Menu_Subtype, id=json_data.get("menu_subtype"))
            unit_category = get_object_or_404(UnitCategory, id=json_data.get("unit_category"))

            new_inventory = inventory_serializer.save(
                menu_type=menu_type,
                menu_subtype=menu_subtype,
                unit_category=unit_category,
                restaurant=request.user.restaurant,
            )

            # Save image file if provided
            if image_file:
                new_inventory.image = image_file
                new_inventory.save()

            inventory_output_serializer = InventoryOutputSerializer(
                new_inventory, context={"request": request}
            )

            response_data = {
                "status": status.HTTP_201_CREATED,
                "error": False,
                "detail": [],
                "message": "Inventory created successfully.",
                "data": inventory_output_serializer.data,
            }
            return Response(response_data, status=status.HTTP_201_CREATED)
        else:
            return Response(
                {"message": "Validation error", "errors": inventory_serializer.errors},
                status=status.HTTP_400_BAD_REQUEST,
            )
    
    # def post(self, request):
    #     menu_type = request.data.get("menu_type")
    #     menu_subtype = request.data.get("menu_subtype")
    #     unit_category = request.data.get("unit_category")
    #     restaurant = request.user.restaurant

    #     if not menu_subtype or not menu_type or not unit_category:
    #         return Response(
    #             {"message": "Validation error"},
    #             status=status.HTTP_404_NOT_FOUND,
    #         )
    #     try:
    #         menu_type = get_object_or_404(MenuTypes, id=menu_type)
    #     except Http404:
    #         return Response(
    #             {"message": "menu type not found"},
    #             status=status.HTTP_404_NOT_FOUND,
    #         )
    #     try:
    #         menu_subtype = get_object_or_404(Menu_Subtype, id=menu_subtype)
    #     except Http404:
    #         return Response(
    #             {"message": "menu subtype not found"},
    #             status=status.HTTP_404_NOT_FOUND,
    #         )
    #     try:
    #         unit_category = get_object_or_404(UnitCategory, id=unit_category)
    #     except Http404:
    #         return Response(
    #             {"message": "unit not found"},
    #             status=status.HTTP_404_NOT_FOUND,
    #         )
    #     inventory_serializer = InventoryInputSerializer(data=request.data)
    #     if inventory_serializer.is_valid(raise_exception=True):
    #         new_inventory = inventory_serializer.save(
    #             menu_type=menu_type,
    #             menu_subtype=menu_subtype,
    #             unit_category=unit_category,
    #             restaurant=restaurant,
    #         )
    #         inventory_output_serializer = InventoryOutputSerializer(
    #             new_inventory, context={"request": request}
    #         )
    #     response_data = {
    #         "status": status.HTTP_200_OK,
    #         "error": False,
    #         "detail": [],
    #         "message": "Inventory created successfully.",
    #     }
    #     return Response(response_data, status=status.HTTP_200_OK)


class InventoryDeleteApiView(APIView):
    permission_classes = [permissions.IsAuthenticated, IsRestaurant]

    def delete(self, request, inventory_Id):
        restaurant = request.user.restaurant

        try:
            inventory = get_object_or_404(Inventory, id=inventory_Id)
        except Http404:
            return Response(
                {"message": "inventory not found"},
                status=status.HTTP_404_NOT_FOUND,
            )
        if restaurant.id != inventory.restaurant.id:
            response_data = {
                "status": status.HTTP_401_UNAUTHORIZED,
                "error": False,
                "detail": "",
                "message": "you are not authorized to perform this action.",
            }
            return Response(response_data, status=status.HTTP_401_UNAUTHORIZED)

        if inventory:
            inventory.delete()
            response_data = {
                "status": status.HTTP_200_OK,
                "error": False,
                "detail": "",
                "message": "inventory deleted successfully.",
            }
            return Response(response_data, status=status.HTTP_200_OK)


class RestaurantInventoryListApiView(APIView):
    """
    Api to list inventory of a restaurant by restaurant_id.
    """

    def get(self, request, restaurant_id, table_id):
        restaurant_id = restaurant_id
        table_id = table_id
        menu_type = request.query_params.get("menu_type")
        subtype = request.query_params.get("subtype")

        filters = {"restaurant": restaurant_id}

        if menu_type:
            filters["menu_type__name"] = menu_type

        if subtype:
            filters["menu_subtype__name"] = subtype

        inventory = Inventory.objects.filter(**filters)

        if not inventory.exists():
            return Response(
                {"message": "Inventory not found"},
                status=status.HTTP_404_NOT_FOUND,
            )
        inventory_output_serializer = InventoryOutputSerializer(
            inventory, context={"request": request}, many=True
        )
        response_data = {
            "status": status.HTTP_200_OK,
            "error": False,
            "detail": inventory_output_serializer.data,
            "message": "",
            "table_id": table_id,
        }
        return Response(response_data, status=status.HTTP_200_OK)


class InventoryUpdateApiView(APIView):
    permission_classes = [permissions.IsAuthenticated, IsRestaurant]

    def put(self, request, inventory_id):
        restaurant = request.user.restaurant
        try:
            inventory = get_object_or_404(Inventory, id=inventory_id)
        except Http404:
            return Response(
                {"message": "inventory not found"},
                status=status.HTTP_404_NOT_FOUND,
            )
        if restaurant.id != inventory.restaurant.id:
            response_data = {
                "status": status.HTTP_401_UNAUTHORIZED,
                "error": False,
                "detail": "",
                "message": "you are not authorized to perform this action.",
            }
            return Response(response_data, status=status.HTTP_401_UNAUTHORIZED)
        inventory_input_serializer = InventoryInputSerializer(
            inventory, data=request.data
        )
        if inventory_input_serializer.is_valid(raise_exception=True):
            updated_inventory = inventory_input_serializer.save()
            updated_restaurant_serializer = InventoryOutputSerializer(
                updated_inventory, context={"request": request}
            )
            response_data = {
                "status": status.HTTP_200_OK,
                "error": False,
                "detail": updated_restaurant_serializer.data,
                "message": "",
            }
            return Response(response_data, status=status.HTTP_200_OK)


class InventoryDetailApiView(APIView):

    """
    Api view to get detail of inventory by id.
    """

    permission_classes = []

    def get(self, request, inventory_id):
        try:
            inventory = get_object_or_404(Inventory, id=inventory_id)
        except Http404:
            return Response(
                {"message": "inventory not found"},
                status=status.HTTP_404_NOT_FOUND,
            )

        inventory_output_serializer = InventoryOutputSerializer(inventory)
        response_data = {
            "status": status.HTTP_200_OK,
            "error": False,
            "detail": inventory_output_serializer.data,
            "message": "",
        }
        return Response(response_data, status=status.HTTP_200_OK)
