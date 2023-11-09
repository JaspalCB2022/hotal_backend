from rest_framework import serializers
from restaurant.models import Inventory


class InventoryInputSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=20)
    item_image = serializers.ImageField()
    description = serializers.CharField()
    total_quantity = serializers.IntegerField()
    available_quantity = serializers.IntegerField()
    unit_price = serializers.DecimalField(decimal_places=2, max_digits=5)


class InventoryOutputSerializer(serializers.ModelSerializer):
    class Meta:
        model = Inventory
        fields = "__all__"
