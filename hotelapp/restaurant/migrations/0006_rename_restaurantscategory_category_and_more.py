# Generated by Django 4.2.7 on 2023-11-07 11:03

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('restaurant', '0005_rename_restaurant_id_restauranttable_restaurant'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='RestaurantsCategory',
            new_name='Category',
        ),
        migrations.RenameModel(
            old_name='RestaurantTable',
            new_name='Table',
        ),
        migrations.AlterModelOptions(
            name='category',
            options={'verbose_name': 'Category', 'verbose_name_plural': 'Categories'},
        ),
        migrations.AlterModelOptions(
            name='table',
            options={'verbose_name': 'Table', 'verbose_name_plural': 'Table'},
        ),
    ]