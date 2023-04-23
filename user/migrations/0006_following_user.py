# Generated by Django 4.2 on 2023-04-23 09:20

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("user", "0005_following_delete_userfollowing"),
    ]

    operations = [
        migrations.AddField(
            model_name="following",
            name="user",
            field=models.ForeignKey(
                default="",
                on_delete=django.db.models.deletion.CASCADE,
                related_name="followers",
                to=settings.AUTH_USER_MODEL,
            ),
        ),
    ]