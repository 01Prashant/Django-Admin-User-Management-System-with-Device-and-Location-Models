# Generated by Django 4.2.3 on 2023-07-04 05:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("Admin_User_App", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="user",
            name="contact",
            field=models.PositiveIntegerField(blank=True, null=True),
        ),
    ]