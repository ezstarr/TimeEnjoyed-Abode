from django.db import models
from django.forms import ModelForm
from django.contrib.auth.models import User


# Create your models here.
# Model: info about data
# Migration: SQL information used to create table
# Make-migration generates files (migrations aka sql equivalent of a model)

class Suggestion(models.Model):
    """Suggestions submitted by people"""

    text = models.TextField()
    date_added = models.DateTimeField(auto_now_add=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)


    def __str__(self):
        return self.text


# class Blog(models.Model):
#     title = models.CharField(max_length=200)
#     entry = models.TextField()
#     last_modified = models.DateTimeField(auto_now_add=True)
#     img = models.ImageField(upload_to="images/")
#
#     # renames the instances of the model
#     # with their title name
#     def __str__(self):
#         return self.title