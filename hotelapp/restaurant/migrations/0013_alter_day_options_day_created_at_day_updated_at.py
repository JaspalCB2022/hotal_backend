# Generated by Django 4.2.7 on 2023-11-09 05:17

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('restaurant', '0012_restaurant_email_restaurant_logo_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='day',
            options={'ordering': ['-created_at']},
        ),
        migrations.AddField(
            model_name='day',
            name='created_at',
            field=models.DateTimeField(db_index=True, default=django.utils.timezone.now),
        ),
        migrations.AddField(
            model_name='day',
            name='updated_at',
            field=models.DateTimeField(auto_now=True),
        ),
    ]