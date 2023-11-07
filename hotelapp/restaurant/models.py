from django.db import models
from django.utils import timezone
from datetime import timedelta, datetime

# Create your models here.
class BaseModel(models.Model):
    created_at = models.DateTimeField(db_index=True, default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class RestaurantsCategory(BaseModel):
    name = models.CharField(max_length=300)
    description = models.CharField(max_length=500,blank=True,null=True)


    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = "Restaurant Category"
        verbose_name_plural = "Restaurant Categories"


class Restaurant(BaseModel):
    name = models.CharField(max_length=300)
    description = models.CharField(max_length=500)
    opening_time = models.TimeField()
    closing_time = models.TimeField()
    phone_number = models.CharField(max_length=20)
    address = models.TextField()
    restaurant_category = models.ForeignKey(RestaurantsCategory, on_delete=models.CASCADE, related_name='restaurants',)

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
        hours = total_seconds / 3600
        minutes = (total_seconds % 3600) // 60
        return f"{hours}:{minutes}"