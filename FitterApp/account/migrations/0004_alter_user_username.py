# Generated by Django 4.2.7 on 2023-11-16 01:23

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("account", "0003_alter_user_username"),
    ]

    operations = [
        migrations.AlterField(
            model_name="user",
            name="username",
            field=models.CharField(
                blank=True,
                max_length=15,
                null=True,
                unique=True,
                validators=[
                    django.core.validators.RegexValidator(
                        code="invalid_username",
                        message="Username must be a valid Mobile Number",
                        regex="^\\d{10,15}$",
                    )
                ],
            ),
        ),
    ]
