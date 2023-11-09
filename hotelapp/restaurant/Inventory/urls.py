from django.urls import path
from .views import InventoryListApiView

urlpatterns = [
    path("list/", InventoryListApiView.as_view(), name="list_restaurant_inventory"),
]
