# Generated by Django 4.1.6 on 2023-02-12 20:01

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("flight", "0002_rename_flightairport_flightjuncture_and_more"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="flight",
            name="availability",
        ),
        migrations.RemoveField(
            model_name="flight",
            name="date",
        ),
    ]
