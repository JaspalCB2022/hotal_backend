from django.shortcuts import get_object_or_404
from django.http import Http404
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from rest_framework import authentication, permissions
from .models import Table, TableQR
from .permissions import IsSuperAdmin

class TableCreateApiView(APIView):
    permission_classes = [permissions.IsAuthenticated,IsSuperAdmin]
    pass
    