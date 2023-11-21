from django.urls import path
from .views import CreateDineInOrderApiView

urlpatterns = [
    path("create/", CreateDineInOrderApiView.as_view(), name="create_order"),
]
