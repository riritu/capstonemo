# Generated by Django 4.2.5 on 2023-10-15 10:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('coreapp', '0027_alter_tenants_tent_uname'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tenants',
            name='tent_name',
            field=models.CharField(max_length=254),
        ),
    ]
