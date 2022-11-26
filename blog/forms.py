from django import forms
from django.forms import ModelForm
from .models import Post


class PostForm(ModelForm):
    class Meta:
        model = Post
        fields = '__all__'

        """class Post(models.Model):
    title = models.CharField(max_length=255)
    tldr = models.CharField(max_length=255)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    slug = models.SlugField(max_length=250, null=True, blank=True)
    body = RichTextField(blank=True, null=True)
    published_at = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)"""

        widgets = {
            "title": forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Give your blog entry a title.'})
        }
