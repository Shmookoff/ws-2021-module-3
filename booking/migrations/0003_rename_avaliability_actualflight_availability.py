# Generated by Django 4.1.6 on 2023-02-12 20:38

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("booking", "0002_alter_passenger_booking"),
    ]

    operations = [
        migrations.RenameField(
            model_name="actualflight",
            old_name="avaliability",
            new_name="availability",
        ),
    ]
