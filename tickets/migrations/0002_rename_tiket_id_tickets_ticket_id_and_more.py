# Generated by Django 4.0.1 on 2022-01-14 08:07

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tickets', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='tickets',
            old_name='tiket_id',
            new_name='ticket_id',
        ),
        migrations.RenameField(
            model_name='tickets',
            old_name='tiket_num',
            new_name='ticket_num',
        ),
    ]
