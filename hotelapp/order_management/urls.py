from django.urls import path
from .views import CreateOrderApiView, ListOrderApiView

urlpatterns = [
    path("create/", CreateOrderApiView.as_view(), name="create_order"),
    path("list/", ListOrderApiView.as_view(), name="list_order"),
]
