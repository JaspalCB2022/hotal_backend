from django.urls import path
from .views import InventoryApiView

urlpatterns = [
    path("list/", InventoryApiView.as_view, name="list_restaurant_inventory")
]
