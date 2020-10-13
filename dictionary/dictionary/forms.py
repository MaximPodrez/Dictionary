from django import forms
from .models import Dictionary, Text, Word


class WordListForm(forms.Form):
    sort_field = forms.ChoiceField(choices=(
        ('frequency', 'frequency ↑'), ('-frequency', 'frequency ↓'), ('label', 'name ↑'), ('-label', 'name ↓')),
        required=False)
    search = forms.CharField(required=False)


class DictionaryForm(forms.ModelForm):
    class Meta(object):
        model = Dictionary
        fields = '__all__'


class TextForm(forms.ModelForm):
    file = forms.FileField(label='Select a file')

    class Meta(object):
        model = Text
        fields = []


class WordForm(forms.ModelForm):
    class Meta(object):
        model = Word
        fields = ['label']
