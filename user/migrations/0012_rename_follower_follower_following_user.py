# Generated by Django 4.2 on 2023-04-23 10:08

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("user", "0011_rename_following_user_follower_follower"),
    ]

    operations = [
        migrations.RenameField(
            model_name="follower",
            old_name="follower",
            new_name="following_user",
        ),
    ]
