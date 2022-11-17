from django import forms
from django.forms import ModelForm
from .models import Suggestion, Profile
from django.utils.translation import gettext_lazy as _

# Link to Diff Field Types:
# https://docs.djangoproject.com/en/4.1/ref/forms/fields/


class ProfileForm(ModelForm):
    class Meta:
        model = Profile
        fields = ['user_mbti', 'childhood_hobbies']
        labels = {'user_mbti': _("Your MBTI"), 'childhood_hobbies': _('Childhood hobbies')}
        help_texts = {
            'user_mbti': _("If you don't know your mbti, take the test <a href='https://www.link.com'>here</a>!"),
            'childhood_hobbies': _("We are trying to see if there's a correlation between MBTI and childhood hobbies. "
                                   "Feel free to share here!"),
            }
        test_item = {'user_mbti': 'Test user_mbti'}


class SuggestionForm(ModelForm):
    class Meta:
        model = Suggestion
        fields = ['text', 'owner']
        check = forms.BooleanField()
        # fields_required = ['field1'] ?


# class BlogForm(forms.Form):
#     model = Blog
#     check = forms.BooleanField()


class CreateNewList(forms.Form):
    name = forms.CharField(label="Name", max_length=200)
    check = forms.BooleanField(required=False)
