# Generated by Django 4.1 on 2023-02-11 22:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0007_remove_post_public_alter_post_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='category',
            name='name',
            field=models.CharField(default='General', max_length=30),
        ),
    ]
