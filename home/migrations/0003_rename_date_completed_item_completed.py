# Generated by Django 4.1 on 2023-01-27 02:18

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0002_rename_date_completed_todolist_completed'),
    ]

    operations = [
        migrations.RenameField(
            model_name='item',
            old_name='date_completed',
            new_name='completed',
        ),
    ]
