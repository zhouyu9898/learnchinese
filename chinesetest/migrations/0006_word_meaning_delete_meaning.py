# Generated by Django 4.0.6 on 2022-09-05 10:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chinesetest', '0005_word_hsk'),
    ]

    operations = [
        migrations.AddField(
            model_name='word',
            name='meaning',
            field=models.CharField(default='ok', max_length=100),
        ),
        migrations.DeleteModel(
            name='Meaning',
        ),
    ]
