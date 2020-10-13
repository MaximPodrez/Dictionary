from django.db import models
from django.urls import reverse


class Dictionary(models.Model):
    title = models.CharField(max_length=200)
    creation_date = models.DateTimeField(auto_now_add=True)

    def get_absolute_url(self):
        return reverse('dictionary:dictionary-info-view', args=[self.id])

    def __str__(self):
        return f"{self.title}"

    class Meta:
        verbose_name = 'dictionary'
        verbose_name_plural = 'dictionaries'


class Text(models.Model):
    title = models.CharField(max_length=255)
    text = models.TextField()
    creation_date = models.DateTimeField(auto_now_add=True)
    dictionary = models.ForeignKey(Dictionary, related_name='texts', on_delete=models.CASCADE)

    def get_absolute_url(self):
        return reverse('dictionary:text-info-view',  kwargs={'pk_dict': self.dictionary.pk, 'pk': self.id})

    def __str__(self):
        return f"{self.title}"


class Word(models.Model):
    label = models.CharField(max_length=255)
    frequency = models.BigIntegerField()
    dictionary = models.ForeignKey(Dictionary, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return f"{self.label}"

    class Meta:
        ordering = ["-frequency"]

