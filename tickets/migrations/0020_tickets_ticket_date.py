# Generated by Django 4.0.1 on 2022-01-19 10:14

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('tickets', '0019_tickets_wait_time'),
    ]

    operations = [
        migrations.AddField(
            model_name='tickets',
            name='ticket_date',
            field=models.DateField(default=django.utils.timezone.now),
            preserve_default=False,
        ),
    ]
