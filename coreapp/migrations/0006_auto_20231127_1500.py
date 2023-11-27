# Generated by Django 3.2.23 on 2023-11-27 07:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0013_auto_20231127_1500'),
        ('coreapp', '0005_alter_admin_pword_alter_admin_uname'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tenants',
            name='groups',
            field=models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='tenant_groups', related_query_name='user', to='auth.Group', verbose_name='groups'),
        ),
        migrations.AlterField(
            model_name='tenants',
            name='user_permissions',
            field=models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='tenant_permissions', related_query_name='user', to='auth.Permission', verbose_name='user permissions'),
        ),
    ]
