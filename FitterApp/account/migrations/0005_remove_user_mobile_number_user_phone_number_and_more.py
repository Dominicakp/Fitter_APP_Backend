# Generated by Django 4.2.7 on 2023-11-16 11:59

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("account", "0004_alter_user_username"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="user",
            name="mobile_number",
        ),
        migrations.AddField(
            model_name="user",
            name="phone_number",
            field=models.CharField(blank=True, max_length=15, null=True, unique=True),
        ),
        migrations.AlterField(
            model_name="user",
            name="username",
            field=models.CharField(blank=True, max_length=30, null=True, unique=True),
        ),
    ]
