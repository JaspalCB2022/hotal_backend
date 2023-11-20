from django.db import models
from django.utils import timezone
from datetime import timedelta, datetime


# Create your models here.
class BaseModel(models.Model):
    created_at = models.DateTimeField(db_index=True, default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True
        ordering = ["-created_at"]


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
    description = models.TextField()
    opening_time = models.TimeField()
    closing_time = models.TimeField()
    phone_number = models.CharField(max_length=20)
    address = models.TextField()
    restaurant_category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        related_name="restaurants",
    )
    is_open_on_sunday = models.BooleanField(default=False)
    is_open_on_monday = models.BooleanField(default=False)
    is_open_on_tuesday = models.BooleanField(default=False)
    is_open_on_wednesday = models.BooleanField(default=False)
    is_open_on_thursday = models.BooleanField(default=False)
    is_open_on_friday = models.BooleanField(default=False)
    is_open_on_saturday = models.BooleanField(default=False)
    email = models.EmailField()
    logo = models.ImageField(
        upload_to="restaurants",
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
    qrlink = models.ImageField(
        upload_to="table_qrcodes",
        null=True,
        blank=True,
    )
    is_active = models.BooleanField(default=False)

    class Meta:
        verbose_name = "Table"
        verbose_name_plural = "Table"

    def __str__(self):
        return f"{self.restaurant.name} - {self.tablenumber}"

   

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
    CATEGORY = (("veg", "Veg"), ("non-veg", "Non-Veg"), ("other", "Other"), ("all", "All"))

    item_categorytype = models.CharField(max_length=20, choices=CATEGORY, null=True, default='all')
    name = models.CharField(max_length=20)
    restaurant = models.ForeignKey(
        Restaurant, on_delete=models.CASCADE, related_name="inventories"
    )
    video_link = models.URLField(max_length=200)
    item_image = models.ImageField(max_length=200)
    description = models.CharField(max_length=200)
    menu_type = models.ForeignKey(
        MenuTypes, on_delete=models.CASCADE, related_name="menu_types"
    )
    menu_subtype = models.ForeignKey(
        Menu_Subtype, on_delete=models.CASCADE, related_name="menu_subtypes"
    )
    total_quantity = models.PositiveIntegerField()
    available_quantity = models.PositiveIntegerField()
    unit_price = models.DecimalField(max_digits=5, decimal_places=2)
    unit_category = models.ForeignKey(
        UnitCategory, on_delete=models.CASCADE, related_name="unit_categories"
    )
    class Meta:
        verbose_name = "Inventory"
        verbose_name_plural = "Inventories"

    def __str__(self):
        return self.name
