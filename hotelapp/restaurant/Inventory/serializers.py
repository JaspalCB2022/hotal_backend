from rest_framework import serializers
from restaurant.models import Restaurant


class RestaurantInputSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=300)
    description = serializers.CharField(max_length=500)
    opening_time = serializers.TimeField()
    closing_time = serializers.TimeField()
    phone_number = serializers.CharField(max_length=20)
    address = serializers.CharField()

    def validate(self, data):
        opening_time = data.get("opening_time")
        closing_time = data.get("closing_time")
        if opening_time and closing_time:
            if opening_time >= closing_time:
                raise serializers.ValidationError(
                    "Closing time should be after opening time."
                )
        return data

    def create(self, validated_data):
        return Restaurant.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.name = validated_data.get("name", instance.name)
        instance.description = validated_data.get("description", instance.description)
        instance.opening_time = validated_data.get(
            "opening_time", instance.opening_time
        )
        instance.closing_time = validated_data.get(
            "closing_time", instance.closing_time
        )
        instance.phone_number = validated_data.get(
            "phone_number", instance.phone_number
        )
        instance.address = validated_data.get("address", instance.address)
        instance.save()
        return instance


class RestaurantOutputSerializer(serializers.ModelSerializer):
    restaurant_category = serializers.StringRelatedField(read_only=True)
    operating_hours = serializers.SerializerMethodField()

    class Meta:
        model = Restaurant
        fields = "__all__"

    def get_operating_hours(self, obj):
        return obj.get_operating_hours()
