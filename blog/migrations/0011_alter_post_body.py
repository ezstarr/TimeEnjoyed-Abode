# Generated by Django 4.1 on 2023-04-10 09:29

from django.db import migrations
import markdownx.models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0010_alter_post_categories_alter_post_status_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='body',
            field=markdownx.models.MarkdownxField(blank=True, null=True),
        ),
    ]