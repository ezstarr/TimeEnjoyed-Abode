# Generated by Django 4.1 on 2023-02-19 04:04

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0006_deck_tarotanswer_tarotcard_tarotrating_tarotrequest'),
    ]

    operations = [
        migrations.AddField(
            model_name='tarotcard',
            name='deck',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='home.deck'),
        ),
        migrations.AddField(
            model_name='tarotcard',
            name='number',
            field=models.IntegerField(default=1),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='deck',
            name='deck_name',
            field=models.CharField(max_length=30, unique=True),
        ),
    ]
