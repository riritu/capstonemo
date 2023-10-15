# Generated by Django 4.2.5 on 2023-10-15 06:04

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('coreapp', '0020_payment_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tenants',
            name='tent_emel',
            field=models.EmailField(default='custom@example.com', max_length=255, validators=[django.core.validators.EmailValidator()]),
        ),
    ]
