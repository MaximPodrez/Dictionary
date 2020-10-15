from django.db.models import QuerySet
from django.urls import reverse_lazy
from django.views import generic
from django.shortcuts import redirect
from .models import Dictionary, Word, Text
from .forms import WordListForm, DictionaryForm, TextForm, WordForm
import re


class DictionaryListView(generic.ListView):
    template_name = 'dictionary/dictionary_list.html'
    context_object_name = 'dict_list'
    model = Dictionary


class DictionaryDetailView(generic.DetailView):
    template_name = 'dictionary/dictionary_info.html'
    context_object_name = 'dict'
    model = Dictionary


class DictionaryCreateView(generic.CreateView):
    form_class = DictionaryForm
    model = Dictionary
    template_name = 'dictionary/dictionary_create.html'


class TextListView(generic.ListView):
    template_name = 'dictionary/dictionary_text_list.html'
    context_object_name = 'text_list'
    model = Text

    def get_context_data(self, **kwargs):
        context = super(TextListView, self).get_context_data(**kwargs)
        context['dict'] = Dictionary.objects.get(pk=self.kwargs.get('pk'))
        return context

    def get_queryset(self):
        queryset = Dictionary.objects.get(pk=self.kwargs.get('pk')).texts.all()
        return queryset


class TextDetailView(generic.DetailView):
    template_name = 'dictionary/dictionary_text_info.html'
    context_object_name = 'text'
    model = Text


class TextCreteView(generic.FormView):
    form_class = TextForm
    template_name = 'dictionary/dictionary_create_text.html'

    def form_valid(self, form):
        file = form.cleaned_data.get('file')
        dict = Dictionary.objects.get(pk=self.kwargs.get('pk'))
        self.text = dict.texts.create(title=file.name, text=file.read().decode())
        raw_text = re.sub(r'[^\s\w]', '', self.text.text).split()
        my_dict = {}
        for word in raw_text:
            if word.title() not in my_dict:
                my_dict[word.title()] = 0

            my_dict[word.title()] += 1
        for name, frequency in my_dict.items():
            try:
                word = dict.word_set.get(label=name)
                word.frequency += frequency
                word.save()
            except Word.DoesNotExist:
                dict.word_set.create(label=name, frequency=frequency)
        dict.save()
        return redirect(self.get_success_url())

    def get_success_url(self):
        return reverse_lazy('dictionary:text-info-view', kwargs={'pk_dict': self.kwargs.get('pk'), 'pk': self.text.id})


class TextCreateView(generic.CreateView):
    form_class = TextForm
    model = Text
    template_name = 'dictionary/dictionary_create_text.html'

    def form_valid(self, form):
        self.object = form.save(commit=False)
        file = form.cleaned_data.get('file')
        self.object.title = file.name
        self.object.text = file.read().decode()
        dict = Dictionary.objects.get(pk=self.kwargs.get('pk'))
        self.object.dictionary = dict
        self.object.save()
        raw_text = re.sub(r'[^\s\w]', '', self.object.text).split()
        parse_text_dict = {}
        for word in raw_text:
            if word.title() not in parse_text_dict:
                parse_text_dict[word.title()] = 0

            parse_text_dict[word.title()] += 1
        for name, frequency in parse_text_dict.items():
            try:
                word = dict.word_set.get(label=name)
                word.frequency += frequency
                word.save()
            except Word.DoesNotExist:
                dict.word_set.create(label=name, frequency=frequency)
        dict.save()
        return redirect(self.get_success_url())


class TextUpdateView(generic.UpdateView):
    model = Text
    fields = ['title', 'text']
    template_name = 'dictionary/dictionary_update_text.html'

    def dispatch(self, request, *args, **kwargs):
        text = Text.objects.get(pk=self.kwargs.get('pk'))
        raw_text = re.sub(r'[^\s\w]', '', text.text).split()
        self.old_word_list = {}
        for word in raw_text:
            if word.title() not in self.old_word_list:
                self.old_word_list[word.title()] = 0

            self.old_word_list[word.title()] += 1

        return super(TextUpdateView, self).dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        self.object = form.save()
        dict = self.object.dictionary

        raw_text = re.sub(r'[^\s\w]', '', self.object.text).split()
        new_word_list = {}
        for word in raw_text:
            if word.title() not in new_word_list:
                new_word_list[word.title()] = 0

            new_word_list[word.title()] += 1

        for word, count in new_word_list.items():
            if word in self.old_word_list:
                update_word = dict.word_set.get(label=word)
                if count > self.old_word_list[word]:
                    update_word.frequency += (count - self.old_word_list[word])
                elif count < self.old_word_list[word]:
                    update_word.frequency += (self.old_word_list[word] - count)
                update_word.save()
                del self.old_word_list[word]
            else:
                try:
                    update_word = dict.word_set.get(label=word)
                    update_word.frequency += count
                    update_word.save()
                except Word.DoesNotExist:
                    dict.word_set.create(label=word, frequency=new_word_list[word])

        for word, count in self.old_word_list.items():
            try:
                update_word = dict.word_set.get(label=word)
                update_word.frequency -= count
                if update_word.frequency == 0:
                    update_word.delete()
                else:
                    update_word.save()
            except Word.DoesNotExist:
                pass
        return redirect(self.get_success_url())

    def get_success_url(self):
        return reverse_lazy('dictionary:text-info-view', kwargs={'pk_dict': self.kwargs.get('pk_dict'), 'pk': self.kwargs.get('pk')})


class WordListView(generic.ListView):
    template_name = 'dictionary/dictionary_word_list.html'
    context_object_name = 'word_list'
    model = Word
    paginate_by = 10

    def dispatch(self, request, *args, **kwargs):
        # self.sort_field = request.GET.get('sort_field')
        # self.search = request.GET.get("search")
        self.form = WordListForm(request.GET)
        self.form.is_valid()
        return super(WordListView, self).dispatch(request, *args, **kwargs)

    def get_queryset(self):
        queryset = Dictionary.objects.get(pk=self.kwargs.get('pk')).word_set.all()
        if self.form.cleaned_data.get('search'):
            queryset = queryset.filter(label__startswith=self.form.cleaned_data['search'].title())
        if self.form.cleaned_data.get('sort_field'):
            queryset = queryset.order_by(self.form.cleaned_data['sort_field'])
        return queryset

    def get_context_data(self, **kwargs):
        context = super(WordListView, self).get_context_data(**kwargs)
        context['dict'] = Dictionary.objects.get(pk=self.kwargs.get('pk'))
        context['form'] = self.form
        return context


class WordCreateView(generic.CreateView):
    form_class = WordForm
    model = Word
    template_name = 'dictionary/dictionary_create_word.html'

    def form_valid(self, form):
        self.object = form.save(commit=False)
        try:
            Word.objects.get(label=self.object.label.title())
        except Word.DoesNotExist:
            self.object.label = self.object.label.title()
            self.object.frequency = 0
            self.object.dictionary = Dictionary.objects.get(pk=self.kwargs.get('pk'))
            self.object.save()
        return redirect(self.get_success_url())

    def get_success_url(self):
        return reverse_lazy('dictionary:word-list-view', kwargs={'pk': self.kwargs.get('pk')})


class WordUpdateView(generic.UpdateView):
    model = Word
    fields = ['label']
    template_name = 'dictionary/dictionary_update_word.html'

    def form_valid(self, form):
        updated_word = self.get_object().label
        self.object = form.save(commit=False)
        for text in self.object.dictionary.texts.filter(text__icontains=updated_word):
            text.text = re.sub(r'\b' + updated_word + r'\b', self.object.label, text.text, flags=re.I)
            text.save()
        try:
            word = self.object.dictionary.word_set.get(label=self.object.label.title())
            if word.id != self.object.id:
                word.frequency += self.object.frequency
                self.object.delete()
            word.save()
        except Word.DoesNotExist:
            self.object.label = self.object.label.title()
            self.object.save()
        return redirect(self.get_success_url())

    def get_success_url(self):
        return reverse_lazy('dictionary:word-list-view', kwargs={'pk': self.kwargs.get('pk_dict')})


class WordDeleteView(generic.DeleteView):
    model = Word
    template_name = 'dictionary/dictionary_delete_word.html'

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        dict = self.object.dictionary
        texts = dict.texts.filter(text__icontains=self.object.label)
        for text in texts:
            text.text = re.sub(r'\b' + self.object.label + r'\b', '', text.text, flags=re.I)
            text.save()
        return super(WordDeleteView, self).delete(request, *args, **kwargs)

    def get_success_url(self):
        return reverse_lazy('dictionary:word-list-view', kwargs={'pk': self.kwargs.get('pk_dict')})