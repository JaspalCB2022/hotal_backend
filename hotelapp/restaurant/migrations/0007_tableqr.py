# Generated by Django 4.2.7 on 2023-11-07 11:13

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('restaurant', '0006_rename_restaurantscategory_category_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='TableQR',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(db_index=True, default=django.utils.timezone.now)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('qrlink', models.ImageField(blank=True, null=True, upload_to='tableqr/%Y/%m/%d/')),
                ('is_active', models.BooleanField(default=True)),
                ('table', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='table', to='restaurant.table')),
            ],
            options={
                'verbose_name': 'Table QR',
                'verbose_name_plural': 'Table QR',
            },
        ),
    ]
