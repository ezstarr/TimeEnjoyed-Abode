# Generated by Django 4.1 on 2023-02-25 11:38

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0012_rename_datetime_readrequest_date_time'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='readrequest',
            options={'get_latest_by': ['-priority', 'date_time']},
        ),
    ]
