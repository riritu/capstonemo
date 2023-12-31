# Generated by Django 4.2.5 on 2023-11-12 06:00

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('coreapp', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='payment',
            name='status',
            field=models.CharField(choices=[('pending', 'Pending'), ('successful', 'Successful'), ('decline', 'Decline')], default='Pending', max_length=20),
        ),
        migrations.AlterField(
            model_name='booked',
            name='approval_status',
            field=models.CharField(choices=[('pending', 'Pending'), ('approved', 'Approved'), ('declined', 'Declined')], default='Pending', max_length=20),
        ),
        migrations.AlterField(
            model_name='payment',
            name='date',
            field=models.DateField(default=django.utils.timezone.now),
        ),
    ]
