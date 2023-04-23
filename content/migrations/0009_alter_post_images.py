# Generated by Django 4.2 on 2023-04-22 19:32

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("content", "0008_rename_image_post_images"),
    ]

    operations = [
        migrations.AlterField(
            model_name="post",
            name="images",
            field=models.ManyToManyField(
                blank=True, null=True, related_name="posts", to="content.image"
            ),
        ),
    ]
