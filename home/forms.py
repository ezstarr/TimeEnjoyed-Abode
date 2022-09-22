from django import forms
from django.forms import ModelForm
from .models import Suggestion

# Link to Diff Field Types:
# https://docs.djangoproject.com/en/4.1/ref/forms/fields/


class SuggestionForm(ModelForm):
    class Meta:
        model = Suggestion
        fields = ['text', 'owner']
        check = forms.BooleanField()
        # fields_required = ['field1'] ?



# class BlogForm(forms.Form):
#     model = Blog
#     check = forms.BooleanField()