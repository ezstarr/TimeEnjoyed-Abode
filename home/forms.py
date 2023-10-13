from django import forms
from django.forms import ModelForm
from .models import Suggestion, ToDoList, Item, Profile, ReadRequest
from django.utils.translation import gettext_lazy as _


# Link to Diff Field Types:
# https://docs.djangoproject.com/en/4.1/ref/forms/fields/


class ProfileForm(ModelForm):
    class Meta:
        model = Profile
        fields = ['user_mbti', 'user_zodiac', 'childhood_hobbies']
        labels = {'user_mbti': _("Your MBTI"), 'user_zodiac': _("Your Western Zodiac Sign"), 'childhood_hobbies': _('Childhood hobbies')}
        help_texts = {
            'user_mbti': _("If you don't know your mbti, take the test <a "
                           "href='https://www.16personalities.com'>here</a>! View <a href='https://timeenjoyed.dev/stats_mbti' "
                           "%}'>stats</a> "),
            'user_zodiac': _("Click <a href='https://timeenjoyed.dev/stats_zodiac' "
                           "%}'>here</a> to see our star sign stats (only if you want :b)"),
            'childhood_hobbies': _("We are trying to see if there's a correlation between MBTI and childhood hobbies. "
                                   "Feel free to share here!"),
        }


class SuggestionForm(ModelForm):
    class Meta:
        model = Suggestion
        fields = ['text']
        check = forms.BooleanField()
        # fields_required = ['field1'] ?


class CreateNewList(ModelForm):
    class Meta:
        model = ToDoList
        fields = ['text', 'priority']

    # priority = forms.RadioSelect()


class CreateNewItem(ModelForm):
    class Meta:
        model = Item
        fields = ['text']


class ReadRequestForm(ModelForm):
    class Meta:
        model = ReadRequest
        fields = ['rating', 'question']
        labels = {'rating': _("How much did this read resonate on a scale from 1-10?"), 'question': _('Last chance edit question before saving:')}

    RATING_CHOICES = [
        ('00', '1-10'),
        ('1', '1'),
        ('2', '2'),
        ('3', '3'),
        ('4', '4'),
        ('5', '5'),
        ('6', '6'),
        ('7', '7'),
        ('8', '8'),
        ('9', '9'),
        ('10', '10'),
    ]
    rating = forms.CharField(widget=forms.Select(choices=RATING_CHOICES))


    question = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 2})
                              )
