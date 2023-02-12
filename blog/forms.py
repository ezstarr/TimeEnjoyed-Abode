from django import forms
from django.forms import ModelForm
from .models import Post, Category
from django_bleach.forms import BleachField


class PostForm(ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'tldr', 'categories', 'body', 'status']

    title = forms.CharField(max_length=100)
    tldr = forms.CharField(max_length=300)
    categories = forms.ModelMultipleChoiceField(
        queryset=Category.objects.all(),
        widget=forms.CheckboxSelectMultiple(attrs={'id': 'category-override', 'class': 'ck-button'})
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # This sets the 'general' category (id 4) as default checked box.
        self.fields['categories'].initial = Category.objects.filter(id=4)

    STATUS_CHOICES = [
        ('dra', 'Draft'),
        ('pri', 'Private'),
        ('pub', 'Published'),
    ]
    status = forms.ChoiceField(widget=forms.RadioSelect(), choices=STATUS_CHOICES)
