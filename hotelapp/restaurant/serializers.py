from rest_framework import serializers
from . models import Restaurant

class RestaurantInputSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=300)
    description = serializers.CharField(max_length=500)
    opening_time = serializers.TimeField()
    closing_time = serializers.TimeField()
    phone_number = serializers.CharField(max_length=20)
    address = serializers.CharField()

    def validate(self, data):
        opening_time = data.get('opening_time')
        closing_time = data.get('closing_time')
        if opening_time and closing_time:
            if opening_time >= closing_time:
                raise serializers.ValidationError("Closing time should be after opening time.")
        return data
    
    def create(self, validated_data):
        return Restaurant.objects.create(**validated_data)
    
    def update(self, instance, validated_data):
        instance.email = validated_data.get('name', instance.name)
        instance.content = validated_data.get('description', instance.description)
        instance.created = validated_data.get('opening_time', instance.opening_time)
        instance.created = validated_data.get('opening_time', instance.opening_time)
        instance.created = validated_data.get('closing_time', instance.closing_time)
        instance.created = validated_data.get('address', instance.address)
        return instance

    

class RestaurantOutputSerializer(serializers.ModelSerializer):
        class Meta:
            model = Restaurant
            fields = "__all__"
