# Generated by Django 4.2 on 2023-04-23 08:44

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("content", "0010_remove_post_images_post_images"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="post",
            name="images",
        ),
        migrations.AddField(
            model_name="post",
            name="image",
            field=models.ManyToManyField(
                null=True, related_name="posts", to="content.image"
            ),
        ),
    ]
