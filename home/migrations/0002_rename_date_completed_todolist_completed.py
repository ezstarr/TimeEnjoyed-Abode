# Generated by Django 4.1 on 2023-01-27 02:09

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='todolist',
            old_name='date_completed',
            new_name='completed',
        ),
    ]
