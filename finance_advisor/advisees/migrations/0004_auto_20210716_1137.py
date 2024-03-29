# Generated by Django 3.2.5 on 2021-07-16 11:37

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("advisees", "0003_auto_20210716_1113"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="family",
            options={"verbose_name": "Family", "verbose_name_plural": "Families"},
        ),
        migrations.AlterField(
            model_name="advisee",
            name="family",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="members",
                to="advisees.family",
            ),
        ),
    ]
