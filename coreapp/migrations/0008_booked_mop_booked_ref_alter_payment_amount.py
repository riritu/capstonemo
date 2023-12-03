# Generated by Django 4.2.1 on 2023-12-03 08:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('coreapp', '0007_alter_tenants_groups_alter_tenants_user_permissions'),
    ]

    operations = [
        migrations.AddField(
            model_name='booked',
            name='mop',
            field=models.CharField(default='CASH', max_length=255),
        ),
        migrations.AddField(
            model_name='booked',
            name='ref',
            field=models.CharField(default='xyz123', max_length=255),
        ),
        migrations.AlterField(
            model_name='payment',
            name='amount',
            field=models.DecimalField(decimal_places=2, max_digits=10),
        ),
    ]
