# Generated by Django 3.2.5 on 2021-07-16 11:08

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("core", "0004_alter_currency_options"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="customuser",
            options={
                "ordering": ("first_name", "last_name", "username"),
                "verbose_name": "Custom User",
                "verbose_name_plural": "Custom Users",
            },
        ),
    ]