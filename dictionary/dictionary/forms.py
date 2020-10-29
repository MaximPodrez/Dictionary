from django import forms
from .models import Dictionary, Text, Word


class WordListForm(forms.Form):
    sort_field = forms.ChoiceField(choices=(
        ('frequency', 'frequency ↑'), ('-frequency', 'frequency ↓'), ('label', 'name ↑'), ('-label', 'name ↓')),
        required=False, widget=forms.Select(attrs={'class': 'custom-select mr-sm-2', 'id': 'inlineFormCustomSelect'}))
    search = forms.CharField(required=False, widget=forms.TextInput(attrs={'class': 'form-control', 'type': 'text',
                                                                           'placeholder': 'Search...'}))


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


class TextTagsForm(forms.ModelForm):
    class Meta(object):
        model = Text
        fields = ['tags_text']
        widgets = {
            'tags_text': forms.Textarea(attrs={'id': 'comment-content', 'name': 'content',
                                               'class': 'form-control rounded-0', 'placeholder': 'Create comment',
                                               'rows': '33'})
        }
