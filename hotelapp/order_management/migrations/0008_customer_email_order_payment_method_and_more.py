# Generated by Django 4.2.7 on 2023-11-27 05:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('order_management', '0007_alter_order_order_type'),
    ]

    operations = [
        migrations.AddField(
            model_name='customer',
            name='email',
            field=models.EmailField(blank=True, max_length=254, null=True),
        ),
        migrations.AddField(
            model_name='order',
            name='payment_method',
            field=models.CharField(blank=True, choices=[('counter', 'Counter'), ('online', 'Online')], max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='order',
            name='payment_status',
            field=models.CharField(blank=True, choices=[('pending', 'Pending'), ('completed', 'Completed'), ('failed', 'Failed'), ('refunded', 'Refunded'), ('cancelled', 'Cancelled'), ('authorized', 'Authorized')], default='pending', max_length=50, null=True),
        ),
    ]
