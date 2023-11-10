import re
from rest_framework import serializers
from .models import Restaurant


class RestaurantInputSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=300)
    description = serializers.CharField(max_length=500)
    opening_time = serializers.TimeField()
    closing_time = serializers.TimeField()
    phone_number = serializers.CharField(max_length=20)
    address = serializers.CharField()
    email = serializers.EmailField()
    logo = serializers.ImageField()
    is_open_on_sunday = serializers.BooleanField(default=False)
    is_open_on_monday = serializers.BooleanField(default=False)
    is_open_on_tuesday = serializers.BooleanField(default=False)
    is_open_on_wednesday = serializers.BooleanField(default=False)
    is_open_on_thursday = serializers.BooleanField(default=False)
    is_open_on_friday = serializers.BooleanField(default=False)
    is_open_on_saturday = serializers.BooleanField(default=False)

    def validate(self, data):
        opening_time = data.get("opening_time")
        closing_time = data.get("closing_time")
        phone_number = data.get("phone_number")
        logo = data.get("logo")

        if opening_time and closing_time:
            if opening_time >= closing_time:
                raise serializers.ValidationError(
                    "Closing time should be after opening time."
                )
        if phone_number:
            if not re.match(r"^\d{10}$", phone_number):
                raise serializers.ValidationError(
                    "Phone number must contain only digits and must be 10 digits."
                )
        if logo:
            if not logo.name.lower().endswith((".png", ".jpg", ".jpeg")):
                raise serializers.ValidationError("Only image files are allowed.")
            max_size = 5 * 1024 * 1024
            if logo.size > max_size:
                raise serializers.ValidationError(
                    "File size too large. Max size is 5MB."
                )
        return data

    def create(self, validated_data):
        days_data = {
            "is_open_on_sunday",
            "is_open_on_monday",
            "is_open_on_tuesday",
            "is_open_on_wednesday",
            "is_open_on_thursday",
            "is_open_on_friday",
            "is_open_on_saturday",
        }
        restaurant = Restaurant.objects.create(**validated_data)
        return restaurant

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
        instance.email = validated_data.get("email", instance.email)
        days_data = {
            "is_open_on_sunday",
            "is_open_on_monday",
            "is_open_on_tuesday",
            "is_open_on_wednesday",
            "is_open_on_thursday",
            "is_open_on_friday",
            "is_open_on_saturday",
        }
        for day in days_data:
            setattr(instance, day, validated_data.get(day, getattr(instance, day)))
        instance.save()
        return instance


class RestaurantOutputSerializer(serializers.ModelSerializer):
    restaurant_category = serializers.StringRelatedField(read_only=True)
    operating_hours = serializers.SerializerMethodField()
    logo = serializers.SerializerMethodField()

    class Meta:
        model = Restaurant
        fields = "__all__"

    def get_operating_hours(self, obj):
        return obj.get_operating_hours()

    def get_logo(self, obj):
        if obj.logo:
            return self.context["request"].build_absolute_uri(obj.logo.url)
        return None
