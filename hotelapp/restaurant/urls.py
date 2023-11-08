from django.urls import path
from . views import RestaurantCreateApiView
urlpatterns = [
    path("create/",RestaurantCreateApiView.as_view(),name='create_restaurant')
]
