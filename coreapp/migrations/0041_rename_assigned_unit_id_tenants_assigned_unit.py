# Generated by Django 4.2.5 on 2023-10-27 04:28

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('coreapp', '0040_rename_assigned_unit_tenants_assigned_unit_id'),
    ]

    operations = [
        migrations.RenameField(
            model_name='tenants',
            old_name='assigned_unit_id',
            new_name='assigned_unit',
        ),
    ]
