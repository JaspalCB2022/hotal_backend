from rest_framework import serializers
from .models import Order, OrderItem, Customer
from restaurant.Inventory.serializers import InventoryOutputSerializer


class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = "__all__"
        read_only_fields = ["restaurant_id"]


class OrderItemSerializer(serializers.ModelSerializer):
    # inventory = InventoryOutputSerializer(source="inventory_id")

    class Meta:
        model = OrderItem
        fields = "__all__"
        read_only_fields = ["restaurant_id", "inventory"]


class OrderItemOutputSerializer(serializers.ModelSerializer):
    inventory = InventoryOutputSerializer(source="inventory_id")

    class Meta:
        model = OrderItem
        fields = "__all__"
        read_only_fields = ["restaurant_id", "inventory"]


class OrderSerializer(serializers.ModelSerializer):
    order_items = OrderItemSerializer(many=True)
    PAYMENT_METHOD_CHOICES = (
        ("counter", "Counter"),
        ("online", "Online"),
    )
    # PAYMENT_STATUS_CHOICES = (
    #     ("pending", "Pending"),
    #     ("completed", "Completed"),
    #     ("failed", "Failed"),
    #     ("refunded", "Refunded"),
    #     ("cancelled", "Cancelled"),
    #     ("authorized", "Authorized"),
    # )
    # payment_status = serializers.ChoiceField(choices=PAYMENT_STATUS_CHOICES)
    payment_method = serializers.ChoiceField(choices=PAYMENT_METHOD_CHOICES)

    class Meta:
        model = Order
        fields = "__all__"
        read_only_fields = ["customer_id", "restaurant_id", "order_status"]

    def create(self, validated_data):
        order_items_data = validated_data.pop("order_items")
        # TODO: if the payment method is counter then payment status should be pending
        payment_method = validated_data.get("payment_method")
        if payment_method == "counter":
            validated_data["payment_status"] = "pending"
        order = Order.objects.create(**validated_data)
        order_items = []
        for order_item_data in order_items_data:
            restaurant_id = self.context["restaurant"]
            order_item_data["restaurant_id"] = restaurant_id
            order_item = OrderItem.objects.create(**order_item_data)
            order_items.append(order_item)
        order.order_items.add(*order_items)
        return order


class OrderOutputSerializer(serializers.ModelSerializer):
    order_items = OrderItemOutputSerializer(many=True)

    class Meta:
        model = Order
        fields = "__all__"
        read_only_fields = ["customer_id", "restaurant_id", "order_status"]
