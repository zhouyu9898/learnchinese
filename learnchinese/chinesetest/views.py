from django.shortcuts import render, reverse
from django.http import HttpResponse, HttpResponseRedirect
from .models import Word
import random
import unidecode


def index(request):
    return render(request, 'index.html', {'hsks': [i for i in range(1,7)]})

def test(request, hsk):
    words = Word.objects.filter(hsk=hsk)
    context = {'words_list': words, 'hsk': hsk, 'full_test': True}
    return render(request, 'test.html', context)

def check(request):
    correct = 0
    for pinyin, word_id in zip(request.POST.getlist('pinyin'), request.POST.getlist('word_id')):
        w = Word.objects.get(id=int(word_id))
        if unidecode.unidecode(w.pinyin).replace(' ', '').lower() == pinyin:
            w.solved = True
            w.save()
            correct += 1

    print(correct)

    full_test = request.POST.get('full_test')
    if full_test == 'True':
        return HttpResponseRedirect(reverse('chinesetest:test', args=(w.hsk,)))
    else:
        return HttpResponseRedirect(reverse('chinesetest:random', args=(w.hsk,)))


def reset(request, hsk):
    Word.objects.all().filter(hsk=hsk).update(solved=False)

    return HttpResponseRedirect(reverse('chinesetest:test', args=(hsk,)))

def random(request, hsk):
    #TODO: look at django forms to focus on input by default
    word = Word.objects.all().filter(hsk=hsk).filter(solved=False).order_by('?')[0]

    context = {'words_list': [word], 'hsk': hsk, 'full_test':False}

    return render(request, 'test.html', context)