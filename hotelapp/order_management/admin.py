from django.contrib import admin
from .models import Customer, OrderItem, Order


@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ("name", "phone_number", "address", "restaurant_id")
    list_filter = ("restaurant_id",)


@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ("restaurant_id", "inventory_id", "quantity")
    list_filter = ("restaurant_id", "inventory_id")


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "restaurant_id",
        "customer_id",
        "table_no",
        "order_type",
        "order_status",
    )
    list_filter = ("restaurant_id", "order_status", "order_type")
    filter_horizontal = ("order_items",)
