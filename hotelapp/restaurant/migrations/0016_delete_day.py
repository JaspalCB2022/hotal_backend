# Generated by Django 4.2.7 on 2023-11-09 10:29

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('restaurant', '0015_remove_day_day_of_week_remove_restaurant_days_open_and_more'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Day',
        ),
    ]