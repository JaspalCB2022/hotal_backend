# Generated by Django 4.2.7 on 2023-11-20 08:29

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('restaurant', '0004_alter_table_is_active'),
    ]

    operations = [
        migrations.RenameField(
            model_name='inventory',
            old_name='categorytype',
            new_name='item_categorytype',
        ),
    ]