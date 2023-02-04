# Generated by Django 4.1 on 2023-02-03 09:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0006_alter_category_options'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='post',
            name='public',
        ),
        migrations.AlterField(
            model_name='post',
            name='status',
            field=models.CharField(choices=[('dra', 'Draft'), ('pri', 'Privat'), ('pub', 'Published')], default='draft', max_length=10),
        ),
    ]