from django.shortcuts import get_object_or_404
from django.http import Http404
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from rest_framework import authentication, permissions
from .menuserializers import MenuTypeSerializer, MenuSubTypeSerializer
from restaurant.models import MenuTypes, Menu_Subtype
from restaurant.permissions import IsSuperAdmin
from rest_framework.permissions import IsAuthenticated


class MenuTypeListApiView(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = MenuTypeSerializer

    def get(self, request, format=None):
        """
        Return a list of all users.
        """ 
        try:
            #print("Request>>>", self.request.user.restaurant.id)
            menu_type_objects = MenuTypes.objects.filter(restaurant=self.request.user.restaurant.id)
            menu_type_data = [MenuTypeSerializer(menu_type).data for menu_type in menu_type_objects]    
            
            resObj = {'status':status.HTTP_200_OK,'message':'', 'detail':menu_type_data, 'error':False}
            return Response(resObj, status=status.HTTP_200_OK)
        except MenuTypes.DoesNotExist:
            resObj = {'status':status.HTTP_200_OK,'message':'Menu type not exists.', 'detail':[], 'error':False}
            return Response(resObj, status=status.HTTP_200_OK)

class MenuSubTypeListApiView(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = MenuSubTypeSerializer

    def get(self, request,menutype_id ,format=None):
        """
        Return a list of all users.
        """ 
        try:
            menusub_type_objects = Menu_Subtype.objects.filter(menutype=menutype_id)
            menusub_type_data = [MenuSubTypeSerializer(menu_type).data for menu_type in menusub_type_objects]    
            resObj = {'status':status.HTTP_200_OK,'message':'', 'detail':menusub_type_data, 'error':False}
            return Response(resObj, status=status.HTTP_200_OK)
        except MenuTypes.DoesNotExist:
            resObj = {'status':status.HTTP_200_OK,'message':'Menu sub type not exists.', 'detail':[], 'error':False}
            return Response(resObj, status=status.HTTP_200_OK)
