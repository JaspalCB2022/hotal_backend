from django.db import transaction
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from restaurant.models import Inventory
from rest_framework import permissions
from restaurant.permissions import IsRestaurant
from .serializers import OrderSerializer, CustomerSerializer


# Create your views here.


class CreateDineInOrderApiView(APIView):
    """
    Api to create order of type "dine-in","take-away" and "home-delivery".

    home-delivery request object example
    ```
    {
        "order_type": "home-delivery",
        "order_items": [
            {
                "inventory_id": 14,
                "quantity": 2
            },
            {
                "inventory_id": 15,
                "quantity": 1
            }
        ],
        "customer_data": {
            "name": "Ankit",
            "phone_number": "9898989898",
            "address":"mohali"
        },
        "session_id": "abcd1234"
    }
    ```

    take-away request object example
    ```
    {
        "order_type": "take-away",
        "order_items": [
            {
                "inventory_id": 14,
                "quantity": 2
            },
            {
                "inventory_id": 15,
                "quantity": 1
            }
        ],
        "customer_data": {
            "name": "Ankit",
            "phone_number": "9898989898"
        },
        "session_id": "abcd1234"
    }
    ```
    dine-in request object example
    ```
    {
        "order_type": "take-away",
        "table_no":1,
        "order_items": [
            {
                "inventory_id": 14,
                "quantity": 2
            },
            {
                "inventory_id": 15,
                "quantity": 1
            }
        ],
        "customer_data": {
            "name": "Ankit",
            "phone_number": "9898989898"
        },
        "session_id": "abcd1234"
    }
    ```
    """

    permission_classes = [permissions.IsAuthenticated, IsRestaurant]

    @transaction.atomic
    def create_dine_in_order(self, request):
        order_serializer = OrderSerializer(
            data=request.data, context={"request": request}
        )
        customer_serializer = CustomerSerializer(data=request.data["customer_data"])
        if order_serializer.is_valid(
            raise_exception=True
        ) and customer_serializer.is_valid(raise_exception=True):
            ordered_items = order_serializer.validated_data.get("order_items", [])
            for item in ordered_items:
                product = item.get("inventory_id")
                quantity_ordered = item.get("quantity", 0)
                try:
                    inventory_item = Inventory.objects.get(id=product.id)
                except Inventory.DoesNotExist:
                    response_data = {
                        "status": status.HTTP_400_BAD_REQUEST,
                        "error": True,
                        "detail": "",
                        "message": f"Product {product} not found in inventory",
                    }
                    return Response(response_data, status=status.HTTP_400_BAD_REQUEST)

                if inventory_item.available_quantity < quantity_ordered:
                    response_data = {
                        "status": status.HTTP_400_BAD_REQUEST,
                        "error": True,
                        "detail": "",
                        "message": f"Insufficient quantity for product {product}",
                    }
                    return Response(response_data, status=status.HTTP_400_BAD_REQUEST)

            customer = customer_serializer.save(restaurant_id=request.user.restaurant)
            order = order_serializer.save(
                order_type="dine-in",
                customer_id=customer,
                restaurant_id=request.user.restaurant,
            )
            for item in order.order_items.all():
                print(item)
                inventory_item = Inventory.objects.get(id=item.inventory_id.id)
                inventory_item.available_quantity -= item.quantity
                inventory_item.save()
            response_data = {
                "status": status.HTTP_201_CREATED,
                "error": False,
                "detail": {
                    "order": order_serializer.data,
                    "customer": customer_serializer.data,
                },
                "message": "",
            }
            return Response(response_data, status=status.HTTP_201_CREATED)

    def create_take_away_order(self, request):
        order_serializer = OrderSerializer(
            data=request.data, context={"request": request}
        )
        customer_serializer = CustomerSerializer(data=request.data["customer_data"])
        if order_serializer.is_valid(
            raise_exception=True
        ) and customer_serializer.is_valid(raise_exception=True):
            ordered_items = order_serializer.validated_data.get("order_items", [])
            for item in ordered_items:
                product = item.get("inventory_id")
                quantity_ordered = item.get("quantity", 0)
                try:
                    inventory_item = Inventory.objects.get(id=product.id)
                except Inventory.DoesNotExist:
                    response_data = {
                        "status": status.HTTP_400_BAD_REQUEST,
                        "error": True,
                        "detail": "",
                        "message": f"Product {product} not found in inventory",
                    }
                    return Response(response_data, status=status.HTTP_400_BAD_REQUEST)

                if inventory_item.available_quantity < quantity_ordered:
                    response_data = {
                        "status": status.HTTP_400_BAD_REQUEST,
                        "error": True,
                        "detail": "",
                        "message": f"Insufficient quantity for product {product}",
                    }
                    return Response(response_data, status=status.HTTP_400_BAD_REQUEST)

            customer = customer_serializer.save(restaurant_id=request.user.restaurant)
            order = order_serializer.save(
                order_type="take-away",
                customer_id=customer,
                restaurant_id=request.user.restaurant,
            )
            for item in order.order_items.all():
                inventory_item = Inventory.objects.get(id=item.inventory_id.id)
                inventory_item.available_quantity -= item.quantity
                inventory_item.save()
            response_data = {
                "status": status.HTTP_201_CREATED,
                "error": False,
                "detail": {
                    "order": order_serializer.data,
                    "customer": customer_serializer.data,
                },
                "message": "",
            }
            return Response(response_data, status=status.HTTP_201_CREATED)

    def create_home_delivery_order(self, request):
        order_serializer = OrderSerializer(
            data=request.data, context={"request": request}
        )
        customer_serializer = CustomerSerializer(data=request.data["customer_data"])
        if order_serializer.is_valid(
            raise_exception=True
        ) and customer_serializer.is_valid(raise_exception=True):
            ordered_items = order_serializer.validated_data.get("order_items", [])
            for item in ordered_items:
                product = item.get("inventory_id")
                quantity_ordered = item.get("quantity", 0)
                try:
                    inventory_item = Inventory.objects.get(id=product.id)
                except Inventory.DoesNotExist:
                    response_data = {
                        "status": status.HTTP_400_BAD_REQUEST,
                        "error": True,
                        "detail": "",
                        "message": f"Product {product} not found in inventory",
                    }
                    return Response(response_data, status=status.HTTP_400_BAD_REQUEST)

                if inventory_item.available_quantity < quantity_ordered:
                    response_data = {
                        "status": status.HTTP_400_BAD_REQUEST,
                        "error": True,
                        "detail": "",
                        "message": f"Insufficient quantity for product {product}",
                    }
                    return Response(response_data, status=status.HTTP_400_BAD_REQUEST)

            customer = customer_serializer.save(restaurant_id=request.user.restaurant)
            order = order_serializer.save(
                order_type="take-away",
                customer_id=customer,
                restaurant_id=request.user.restaurant,
            )
            for item in order.order_items.all():
                inventory_item = Inventory.objects.get(id=item.inventory_id.id)
                inventory_item.available_quantity -= item.quantity
                inventory_item.save()
            response_data = {
                "status": status.HTTP_201_CREATED,
                "error": False,
                "detail": {
                    "order": order_serializer.data,
                    "customer": customer_serializer.data,
                },
                "message": "",
            }
            return Response(response_data, status=status.HTTP_201_CREATED)

    def post(self, request):
        if request.data.get("order_type") == "dine-in":
            if not "customer_data" in request.data:
                response_data = {
                    "status": status.HTTP_400_BAD_REQUEST,
                    "error": True,
                    "detail": "",
                    "message": "Customer Data is required for this order",
                }
                return Response(response_data, status=status.HTTP_400_BAD_REQUEST)
            if not "table_no" in request.data:
                response_data = {
                    "status": status.HTTP_400_BAD_REQUEST,
                    "error": True,
                    "detail": "",
                    "message": "table no is required for this order.",
                }
                return Response(response_data, status=status.HTTP_400_BAD_REQUEST)
            return self.create_dine_in_order(request)

        if request.data.get("order_type") == "take-away":
            if not "customer_data" in request.data:
                response_data = {
                    "status": status.HTTP_400_BAD_REQUEST,
                    "error": True,
                    "detail": "",
                    "message": "Customer Data is required for this order",
                }
                return Response(response_data, status=status.HTTP_400_BAD_REQUEST)
            return self.create_take_away_order(request)

        if request.data.get("order_type") == "home-delivery":
            if not "customer_data" in request.data:
                response_data = {
                    "status": status.HTTP_400_BAD_REQUEST,
                    "error": True,
                    "detail": "",
                    "message": "Customer Data is required for this order",
                }
                return Response(response_data, status=status.HTTP_400_BAD_REQUEST)
            if not request.data["customer_data"].get("address"):
                response_data = {
                    "status": status.HTTP_400_BAD_REQUEST,
                    "error": True,
                    "detail": "",
                    "message": "customer address is required for this order.",
                }
                return Response(response_data, status=status.HTTP_400_BAD_REQUEST)
            return self.create_home_delivery_order(request)
