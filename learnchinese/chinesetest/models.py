from django.db import models

# Create your models here.
class Word(models.Model):
    hanzi = models.CharField(max_length=30)
    pinyin = models.CharField(max_length=30)
    meaning = models.CharField(default='ok', max_length=100)
    solved = models.BooleanField(default=False)
    hsk = models.IntegerField()

    def __str__(self):
        return self.hanzi + " " + self.pinyin