# Generated by Django 4.2.7 on 2023-11-23 07:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('coreapp', '0002_payment_status_alter_booked_approval_status_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='admin',
            name='uname',
            field=models.CharField(default='admin_username', max_length=255),
        ),
    ]
