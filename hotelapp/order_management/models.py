from django.db import models
from django.utils import timezone
from restaurant.models import Restaurant, Table, Inventory


class BaseModel(models.Model):
    created_at = models.DateTimeField(db_index=True, default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True
        ordering = ["-created_at"]


class Customer(BaseModel):
    restaurant_id = models.ForeignKey(
        Restaurant, on_delete=models.CASCADE, related_name="customers"
    )
    name = models.CharField(max_length=200)
    phone_number = models.CharField(max_length=20)
    address = models.TextField()

    def __str__(self):
        return f"{self.name}"


class OrderItem(BaseModel):
    restaurant_id = models.ForeignKey(
        Restaurant, on_delete=models.SET_NULL, related_name="order_items", null=True
    )
    inventory_id = models.ForeignKey(
        Inventory, on_delete=models.SET_NULL, related_name="order_inventory", null=True
    )
    quantity = models.PositiveIntegerField()
    # session_id = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        return f"{self.restaurant_id} - {self.inventory_id}"


class Order(BaseModel):
    ORDER_TYPE_CHOICES = (
        ("dine-in", "Dine in"),
        ("take-away", "Take Away"),
        ("home-delivery", "Home Delivery"),
    )

    ORDER_STATUS_CHOICES = (
        ("pending", "Pending"),
        ("delivered", "Delivered"),
        ("confirmed", "Confirmed"),
        ("cancelled", "Cancelled"),
    )
    restaurant_id = models.ForeignKey(
        Restaurant, on_delete=models.CASCADE, related_name="orders_received"
    )
    customer_id = models.ForeignKey(
        Customer, on_delete=models.SET_NULL, related_name="customer_orders", null=True
    )
    table_no = models.ForeignKey(
        Table, on_delete=models.SET_NULL, related_name="orders_at_table", null=True
    )
    order_type = models.CharField(max_length=20, choices=ORDER_TYPE_CHOICES)
    payment_id = models.CharField(max_length=100, blank=True, null=True)
    order_status = models.CharField(max_length=100, choices=ORDER_STATUS_CHOICES)
    payment_status = models.CharField(max_length=50, blank=True, null=True)
    order_items = models.ManyToManyField(OrderItem, related_name="order_items_in_order")
    session_id = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        return f"Order Id: {self.id}"
