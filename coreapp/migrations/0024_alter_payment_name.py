# Generated by Django 4.2.5 on 2023-10-15 09:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('coreapp', '0023_alter_payment_name_alter_tenants_tent_uname'),
    ]

    operations = [
        migrations.AlterField(
            model_name='payment',
            name='name',
            field=models.CharField(max_length=254),
        ),
    ]
