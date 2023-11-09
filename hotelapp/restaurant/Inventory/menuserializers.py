from rest_framework import serializers
from restaurant.models import MenuTypes, Menu_Subtype
from restaurant.serializers import RestaurantOutputSerializer

class MenuTypeSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = MenuTypes
        fields = ['id','name' ]


class MenuSubTypeSerializer(serializers.ModelSerializer):
    menutype = MenuTypeSerializer(many=False, required=False, )
    class Meta:
        model = Menu_Subtype
        fields = "__all__"