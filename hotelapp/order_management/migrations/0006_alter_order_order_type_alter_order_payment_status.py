# Generated by Django 4.2.7 on 2023-11-24 05:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('order_management', '0005_alter_order_order_status_alter_order_order_type_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='order_type',
            field=models.CharField(choices=[('dine-in', 'Dine in'), ('take-away', 'Take Away'), ('home-delivery', 'Home Delivery')], default='pending', max_length=20),
        ),
        migrations.AlterField(
            model_name='order',
            name='payment_status',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
    ]
