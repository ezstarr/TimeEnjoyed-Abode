# Generated by Django 4.1 on 2022-11-22 09:25

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=30)),
            ],
        ),
        migrations.CreateModel(
            name='Post',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255)),
                ('tldr', models.CharField(max_length=255)),
                ('slug', models.SlugField(blank=True, max_length=250, null=True)),
                ('body', models.TextField(blank=True, null=True)),
                ('published_at', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('category', models.CharField(default=None, max_length=255)),
                ('public', models.BooleanField()),
                ('status', models.CharField(choices=[('dra', 'Draft'), ('pri', 'Private'), ('pub', 'Published')], default='draft', max_length=10)),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('likes', models.ManyToManyField(related_name='liked_posts', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
