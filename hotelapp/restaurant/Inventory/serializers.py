from rest_framework import serializers
from restaurant.models import Inventory


class InventoryInputSerializer(serializers.Serializer):
    CATEGORY = (("veg", "Veg"), ("non-veg", "Non-Veg"), ("other", "Other"))
    name = serializers.CharField(max_length=20)
    video_link = serializers.URLField()
    item_image = serializers.ImageField()
    description = serializers.CharField()
    total_quantity = serializers.IntegerField()
    available_quantity = serializers.IntegerField()
    unit_price = serializers.DecimalField(decimal_places=2, max_digits=5)
    item_categorytype = serializers.ChoiceField(choices=CATEGORY)

    def create(self, validated_data):
        return Inventory.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.name = validated_data.get("name", instance.name)
        instance.description = validated_data.get("description", instance.description)
        instance.item_image = validated_data.get("item_image", instance.item_image)
        instance.total_quantity = validated_data.get(
            "total_quantity", instance.total_quantity
        )
        instance.available_quantity = validated_data.get(
            "available_quantity", instance.available_quantity
        )
        instance.unit_price = validated_data.get("unit_price", instance.unit_price)
        instance.item_categorytype = validated_data.get(
            "item_categorytype", instance.item_categorytype
        )
        instance.save()
        return instance


class InventoryOutputSerializer(serializers.ModelSerializer):
    unit_category = serializers.StringRelatedField()
    menu_subtype = serializers.StringRelatedField()
    menu_type = serializers.StringRelatedField()

    class Meta:
        model = Inventory
        fields = "__all__"

