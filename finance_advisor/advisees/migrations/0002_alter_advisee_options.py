# Generated by Django 3.2.5 on 2021-07-16 11:08

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("advisees", "0001_initial"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="advisee",
            options={
                "ordering": ("first_name", "last_name", "username"),
                "verbose_name": "Advisee",
                "verbose_name_plural": "Advisees",
            },
        ),
    ]
