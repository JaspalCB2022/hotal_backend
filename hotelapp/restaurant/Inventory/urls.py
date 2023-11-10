from django.urls import path
from .views import InventoryListApiView, InventoryCreateApiView

urlpatterns = [
    path("list/", InventoryListApiView.as_view(), name="list_restaurant_inventory"),
    path(
        "create/", InventoryCreateApiView.as_view(), name="create_restaurant_inventory"
    ),
]
