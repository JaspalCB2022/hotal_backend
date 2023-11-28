from django.urls import path
from .views import CreateOrderApiView, ListOrderApiView, AddItemsToCart

urlpatterns = [
    path("create/", CreateOrderApiView.as_view(), name="create_order"),
    path("list/", ListOrderApiView.as_view(), name="list_order"),
    path(
        "add_to_cart/",
        AddItemsToCart.as_view(),
        name="add_items_to_cart",
    ),
]
