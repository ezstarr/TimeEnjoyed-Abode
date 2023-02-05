from django import forms
from django.forms import ModelForm
from .models import Post, Category
from django_bleach.forms import BleachField


class PostForm(ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'tldr', 'categories', 'body', 'status']


    title = forms.CharField(max_length=300)
    tldr = forms.CharField(max_length=50)
    categories = forms.ModelMultipleChoiceField(
        queryset=Category.objects.all(),
        widget=forms.CheckboxSelectMultiple(attrs={'id': 'category-override', 'class': 'ck-button'})
        )
    STATUS_CHOICES = [
        ('dra', 'Draft'),
        ('pri', 'Private'),
        ('pub', 'Published'),
    ]
    status = forms.ChoiceField(widget=forms.RadioSelect(), choices=STATUS_CHOICES)



