from django.contrib import admin
from .models import (
    Restaurant,
    Category,
    Table,
    MenuTypes,
    Menu_Subtype,
    UnitCategory,
    Inventory,
)

# Register your models here.

admin.site.register(Restaurant)
admin.site.register(Category)
admin.site.register(Table)
admin.site.register(MenuTypes)
admin.site.register(Menu_Subtype)
admin.site.register(UnitCategory)
admin.site.register(Inventory)
