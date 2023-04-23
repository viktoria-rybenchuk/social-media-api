# Generated by Django 4.2 on 2023-04-22 20:07

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("content", "0009_alter_post_images"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="post",
            name="images",
        ),
        migrations.AddField(
            model_name="post",
            name="images",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="posts",
                to="content.image",
            ),
        ),
    ]