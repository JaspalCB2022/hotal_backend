from django.urls import path
from .views import InventoryListApiView
from .menuview import MenuTypeListApiView, MenuSubTypeListApiView

urlpatterns = [
    path("list/", InventoryListApiView.as_view(), name="list_restaurant_inventory"),
    path("menutypes/", MenuTypeListApiView.as_view(), name="list_restaurant_menutypes"),
    path("menusubtype/<int:menutype_id>/", MenuSubTypeListApiView.as_view(), name="list_restaurant_menu_sub_type"),
]
