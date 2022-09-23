from django.db import models
from django.conf import settings


class Word(models.Model):
    hanzi = models.CharField(max_length=30)
    pinyin = models.CharField(max_length=30)
    meaning = models.CharField(default='ok', max_length=100)
    hsk = models.IntegerField()

    def __str__(self):
        return self.hanzi + " " + self.pinyin

class Solve(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    word = models.ForeignKey("Word", on_delete=models.CASCADE)