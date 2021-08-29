from django.shortcuts import render
from django.http import HttpResponse
from .models import Word
import random


def index(request):
    words = list(Word.objects.all())
    print(type(words))
    context = {'words_list': list(words)}
    return render(request, 'index.html', context)


def check(request):
    w = Word.objects.filter(id=int(request.POST['word_id']))
    if w[0].pinyin == request.POST['pinyin']:
        w.update(solved=True)

    words = Word.objects.all()
    context = {'words_list': words}
    return render(request, 'index.html', context)


def reset(request):
    pass
    words = Word.objects.all()
    words.update(solved=False)

    context = {'words_list': words}
    return render(request, 'index.html', context)


def shuffle(request):
    pass
    # words = list(Word.objects.all())
    # random.shuffle(words)
    # print(words)
    # context = {'words_list': words}
    # return render(request, 'index.html', context)