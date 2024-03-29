from django import forms
from django.forms import ModelForm
from .models import Post, Category
from markdownx.fields import MarkdownxFormField
from .widgets import PillBoxSelectMultiple


# class MyCustomTextarea(forms.Textarea):
#     template_name = 'markdownx/widget.html'


class PostForm(ModelForm):
    class Meta:
        model = Post
        # fields = '__all__'
        fields = ['title', 'tldr', 'categories', 'body', 'status']

    title = forms.CharField(max_length=100)
    tldr = forms.CharField(max_length=300)
    categories = forms.ModelMultipleChoiceField(
        queryset=Category.objects.all(),
        widget=PillBoxSelectMultiple(attrs={'class': 'pill-container'}))

    body = MarkdownxFormField()


    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # This sets the 'general' category (id 4) as default checked box.
        self.fields['categories'].initial = Category.objects.filter(id=4)

    STATUS_CHOICES = [
        ('dra', 'Draft'),
        ('pri', 'Private'),
        ('pub', 'Published'),
    ]
    status = forms.ChoiceField(widget=forms.Select(attrs={'class': 'button-bar'}), choices=STATUS_CHOICES)

    # my_field = forms.CharField(widget=MyCustomTextarea())
