from django.utils import timezone
from datetime import timedelta
from django.db import transaction
from django.db.models import Q
from django.core.paginator import Paginator
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from restaurant.models import Inventory
from rest_framework import permissions
from restaurant.permissions import IsRestaurant
from restaurant.models import Restaurant

from .serializers import (
    OrderSerializer,
    CustomerSerializer,
    OrderItemOutputSerializer,
    OrderOutputSerializer,
)
from .models import Order

# Create your views here.


class CreateOrderApiView(APIView):
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
        restaurant = request.user.restaurant
        order_serializer = OrderSerializer(
            data=request.data, context={"restaurant": restaurant}
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

    @transaction.atomic
    def create_take_away_order(self, request):
        restaurant = request.user.restaurant
        order_serializer = OrderSerializer(
            data=request.data, context={"restaurant": restaurant}
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
                # order_type="take-away",
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

    @transaction.atomic
    def create_home_delivery_order(self, request):
        restaurant = request.user.restaurant
        order_serializer = OrderSerializer(
            data=request.data, context={"restaurant": restaurant}
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


class ListOrderApiView(APIView):
    """
    A view to list orders based on specified filters for a restaurant.

    URL Structure:
    http://127.0.0.1:8000/api/order/list/?order_type=take-away&search=9636978524&order_status=pending&payment_status=paid&page=1&page_size=5&sort_by=created_at&sort_order=asc&time_filter=yesterday
    """

    permission_classes = [permissions.IsAuthenticated, IsRestaurant]

    def get(self, request):
        restaurant = request.user.restaurant
        order_type = request.query_params.get("order_type")
        order_status = request.query_params.get("order_status")
        payment_status = request.query_params.get("payment_status")
        search_query = request.query_params.get("search")
        page_number = request.query_params.get("page", 1)
        page_size = request.query_params.get("page_size", 10)
        time_filter = request.query_params.get("time_filter")
        sort_by = request.query_params.get("sort_by")
        sort_order = request.query_params.get("sort_order")

        filters = {}

        if order_type:
            filters["order_type"] = order_type
        if order_status:
            filters["order_status"] = order_status
        if payment_status:
            filters["payment_status"] = payment_status
        queryset = Order.objects.filter(restaurant_id=restaurant)

        try:
            if time_filter == "recent":
                today = timezone.now().date()
                orders = queryset.filter(created_at__date=today, **filters)
            elif time_filter == "yesterday":
                yesterday = timezone.now().date() - timedelta(days=1)
                orders = queryset.filter(created_at__date=yesterday, **filters)
            else:
                orders = queryset.filter(**filters)
            if sort_by in [
                "id",
                "table_no",
                "customer_id__phone_number",
                "order_status",
                "created_at",
            ]:
                if sort_order == "asc":
                    orders = orders.order_by(sort_by)
                elif sort_order == "desc":
                    orders = orders.order_by(f"-{sort_by}")
            if search_query:
                orders = orders.filter(
                    Q(id__icontains=search_query)
                    | Q(table_no__tablenumber__icontains=search_query)
                    | Q(customer_id__phone_number__icontains=search_query)
                    | Q(order_status__icontains=search_query)
                    | Q(created_at__icontains=search_query)
                )
            paginator = Paginator(orders, page_size)
            paginated_orders = paginator.page(page_number)
            order_serializer = OrderOutputSerializer(paginated_orders, many=True)
            response_data = {
                "status": status.HTTP_200_OK,
                "error": False,
                "detail": order_serializer.data,
                "message": f"{len(order_serializer.data)} order found.",
                "pagination_info": {
                    "total_pages": paginator.num_pages,
                    "current_page": paginated_orders.number,
                    "total_items": paginator.count,
                    "page_size": paginator.per_page,
                },
            }
            return Response(response_data, status=status.HTTP_200_OK)
        except Order.DoesNotExist:
            response_data = {
                "status": status.HTTP_400_BAD_REQUEST,
                "error": True,
                "detail": "",
                "message": "Orders for the given restaurant not found.",
            }
            return Response(response_data, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            response_data = {
                "status": status.HTTP_400_BAD_REQUEST,
                "error": True,
                "detail": "",
                "message": f"{str(e)}",
            }
            return Response(response_data, status=status.HTTP_400_BAD_REQUEST)


class AddItemsToCart(APIView):
    def post(self, request):
        restaurant_id = request.data.get("restaurant_id")
        restaurant = Restaurant.objects.get(id=restaurant_id)
        order_serializer = OrderSerializer(
            data=request.data, context={"restaurant": restaurant}
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

            customer = customer_serializer.save(restaurant_id=restaurant)
            order = order_serializer.save(
                order_type="dine-in", customer_id=customer, restaurant_id=restaurant
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
