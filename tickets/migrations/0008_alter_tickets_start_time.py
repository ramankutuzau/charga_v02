# Generated by Django 4.0 on 2022-01-14 19:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tickets', '0007_alter_tickets_start_time'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tickets',
            name='start_time',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
