from rest_framework import serializers
from .models import Order, OrderItem, Customer
from restaurant.Inventory.serializers import InventoryOutputSerializer


class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = "__all__"
        read_only_fields = ["restaurant_id"]


class OrderItemSerializer(serializers.ModelSerializer):
    inventory = InventoryOutputSerializer(source="inventory_id")

    class Meta:
        model = OrderItem
        fields = "__all__"
        read_only_fields = ["restaurant_id", "inventory"]


class OrderSerializer(serializers.ModelSerializer):
    order_items = OrderItemSerializer(many=True)

    class Meta:
        model = Order
        fields = "__all__"
        read_only_fields = ["customer_id", "restaurant_id", "order_status"]

    def create(self, validated_data):
        order_items_data = validated_data.pop("order_items")

        order = Order.objects.create(**validated_data)
        order_items = []
        for order_item_data in order_items_data:
            restaurant_id = self.context["request"].user.restaurant
            order_item_data["restaurant_id"] = restaurant_id
            order_item = OrderItem.objects.create(**order_item_data)
            order_items.append(order_item)
        order.order_items.add(*order_items)
        return order
