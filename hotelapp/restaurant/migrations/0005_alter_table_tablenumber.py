# Generated by Django 4.2.7 on 2023-11-20 07:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('restaurant', '0004_alter_table_is_active'),
    ]

    operations = [
        migrations.AlterField(
            model_name='table',
            name='tablenumber',
            field=models.IntegerField(unique=True),
        ),
    ]
