from django.shortcuts import render
from django.http import HttpResponse
from .models import Word
import random
import unidecode


def index(request):
    words = Word.objects.all().order_by('pinyin')
    context = {'words_list': list(words)}
    return render(request, 'index.html', context)


def check(request):
    # print(request.POST.getlist('pinyin'))
    # print(request.POST.getlist('word_id'))
    correct = 0
    for pinyin, word_id in zip(request.POST.getlist('pinyin'), request.POST.getlist('word_id')):
        w = Word.objects.filter(id=int(word_id))
        if unidecode.unidecode(w[0].pinyin).replace(" ", "").lower() == pinyin:
            correct += 1

    print(correct)
    words = Word.objects.all().order_by('pinyin')
    context = {'words_list': words}
    return render(request, 'index.html', context)


def reset(request):
    words = Word.objects.all().update(solved=False)
    words = Word.objects.all().order_by('pinyin')

    context = {'words_list': words}
    return render(request, 'index.html', context)