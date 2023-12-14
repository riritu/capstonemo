# Generated by Django 4.2.1 on 2023-12-07 05:42

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('coreapp', '0008_booked_mop_booked_ref_alter_payment_amount'),
    ]

    operations = [
        migrations.AlterField(
            model_name='booked',
            name='ref',
            field=models.CharField(default="xyz123"),
        ),
        migrations.AlterField(
            model_name='tenants',
            name='tent_emel',
            field=models.EmailField(default='custom@example.com', max_length=255, unique=True, validators=[django.core.validators.EmailValidator()]),
        ),
    ]
