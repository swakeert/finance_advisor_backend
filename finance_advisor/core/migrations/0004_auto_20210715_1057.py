# Generated by Django 3.2.5 on 2021-07-15 10:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("core", "0003_alter_customuser_profile_photo"),
    ]

    operations = [
        migrations.AlterField(
            model_name="customuser",
            name="date_of_birth",
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name="customuser",
            name="profile_photo",
            field=models.ImageField(
                blank=True, default="", upload_to="uploads/profile_photos/"
            ),
            preserve_default=False,
        ),
    ]
