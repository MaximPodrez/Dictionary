# Generated by Django 3.1.2 on 2020-10-22 13:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dictionary', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='text',
            name='tags_text',
            field=models.TextField(default='Hey', max_length=255),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='word',
            name='tags',
            field=models.CharField(default='hey', max_length=255),
            preserve_default=False,
        ),
    ]
