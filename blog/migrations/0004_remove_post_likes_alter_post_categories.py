# Generated by Django 4.1 on 2022-11-27 02:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0003_post_categories_alter_post_likes_alter_post_public'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='post',
            name='likes',
        ),
        migrations.AlterField(
            model_name='post',
            name='categories',
            field=models.ManyToManyField(default='', to='blog.category'),
        ),
    ]
