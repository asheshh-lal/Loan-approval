# Generated by Django 5.0.3 on 2024-03-09 18:23

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("MyAPI", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="approvals",
            name="graduatededucation",
            field=models.CharField(
                choices=[("Graduate", "Graduate"), ("Not_Graduate", "Not_Graduate")],
                max_length=15,
            ),
        ),
    ]