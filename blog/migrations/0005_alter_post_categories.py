# Generated by Django 4.1 on 2022-11-27 02:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0004_remove_post_likes_alter_post_categories'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='categories',
            field=models.ManyToManyField(to='blog.category'),
        ),
    ]