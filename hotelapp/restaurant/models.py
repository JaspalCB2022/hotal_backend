from django.db import models
from django.utils import timezone
from datetime import timedelta, datetime


# Create your models here.
class BaseModel(models.Model):
    created_at = models.DateTimeField(db_index=True, default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Category(BaseModel):
    name = models.CharField(max_length=300)
    description = models.CharField(max_length=500, blank=True, null=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Category"
        verbose_name_plural = "Categories"


class Restaurant(BaseModel):
    name = models.CharField(max_length=300)
    description = models.CharField(max_length=500)
    opening_time = models.TimeField()
    closing_time = models.TimeField()
    phone_number = models.CharField(max_length=20)
    address = models.TextField()
    restaurant_category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        related_name="restaurants",
    )

    class Meta:
        verbose_name = "Restaurant"
        verbose_name_plural = "Restaurants"

    def __str__(self):
        return self.name

    def get_operating_hours(self):
        opening_time = datetime.combine(datetime.now().date(), self.opening_time)
        closing_time = datetime.combine(datetime.now().date(), self.closing_time)
        operating_hours = closing_time - opening_time
        total_seconds = operating_hours.total_seconds()
        hours = int(total_seconds) // 3600
        minutes = (int(total_seconds) % 3600) // 60
        return f"{hours}:{minutes}"


class Table(BaseModel):
    restaurant = models.ForeignKey(
        Restaurant, on_delete=models.CASCADE, related_name="restaurants"
    )
    tablenumber = models.IntegerField()
    capacity = models.IntegerField()
    is_occupied = models.BooleanField(default=False)

    class Meta:
        verbose_name = "Table"
        verbose_name_plural = "Table"

    def __str__(self):
        return self.tablenumber


class TableQR(BaseModel):
    table = models.ForeignKey(Table, on_delete=models.CASCADE, related_name="table")
    qrlink = models.ImageField(
        upload_to="tableqr/%Y/%m/%d/",
        null=True,
        blank=True,
    )
    is_active = models.BooleanField(default=True)

    class Meta:
        verbose_name = "Table QR"
        verbose_name_plural = "Table QR"

    def __str__(self):
        return self.tablenumber


class MenuTypes(BaseModel):
    name = models.CharField(max_length=20)
    restaurant = models.ForeignKey(
        Restaurant, on_delete=models.CASCADE, related_name="menutypes"
    )

    class Meta:
        verbose_name = "Menu Types"
        verbose_name_plural = "Menu Types"

    def __str__(self):
        return self.name


class Menu_Subtype(BaseModel):
    CATEGORY = (
        ("veg", "Veg"),
        ("non-veg", "Non-Veg"),
    )
    categorytype = models.CharField(
        max_length=20, choices=CATEGORY, null=True, default=None
    )
    name = models.CharField(max_length=20)
    menutype = models.ForeignKey(
        MenuTypes, on_delete=models.CASCADE, related_name="menusubtypes"
    )

    class Meta:
        verbose_name = "Menu Subtype"
        verbose_name_plural = "Menu Subtypes"

    def __str__(self):
        return self.name


class UnitCategory(models.Model):
    UNIT_CHOICES = (
        ("ml", "Milliliters (ml)"),
        ("g", "Grams (g)"),
        ("pcs", "Pieces (pcs)"),
        ("plate", "Plates"),
        ("cup", "Cups"),
    )

    name = models.CharField(
        max_length=20, unique=True, help_text="Name of the unit category"
    )
    abbreviation = models.CharField(
        max_length=5, choices=UNIT_CHOICES, help_text="Unit abbreviation"
    )

    class Meta:
        verbose_name = "Unit Category"
        verbose_name_plural = "Unit Categories"

    def __str__(self):
        return self.name


class Inventory(BaseModel):
    CATEGORY = (("veg", "Veg"), ("non-veg", "Non-Veg"), ("other", "Other"))

    name = models.CharField(max_length=20)
    restaurant = models.ForeignKey(
        Restaurant, on_delete=models.CASCADE, related_name="inventories"
    )
    video_link = models.URLField(max_length=200)
    item_image = models.URLField(max_length=200)
    description = models.CharField(max_length=200)
    menu_type = models.ForeignKey(
        MenuTypes, on_delete=models.CASCADE, related_name="menu_types"
    )
    menu_subtype = models.ForeignKey(
        Menu_Subtype, on_delete=models.CASCADE, related_name="menu_subtypes"
    )
    total_quantity = models.PositiveIntegerField()
    available_quantity = models.PositiveIntegerField()
    unit_price = models.PositiveIntegerField()
    unit_category = models.ForeignKey(
        UnitCategory, on_delete=models.CASCADE, related_name="unit_categories"
    )

    class Meta:
        verbose_name = "Inventory"
        verbose_name_plural = "Inventories"

    def __str__(self):
        return self.name
