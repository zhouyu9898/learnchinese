from django.shortcuts import render, reverse
from django.http import HttpResponse, HttpResponseRedirect
from django.db.models.query import EmptyQuerySet
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from .models import Word
from .forms import TestForm
import random
import unidecode


def index(request):
    hsks = [i for i in range(1,7)]
    solved_counts = []
    total_counts = []
    for hsk in hsks:
        words = Word.objects.filter(hsk=hsk)
        total_counts.append(words.count())
        solved_counts.append(words.filter(solved=True).count())

    context = {
        'hsks': zip(hsks, solved_counts, total_counts)
    }        

    return render(request, 'index.html', context)

def test(request, hsk):
    words = Word.objects.filter(hsk=hsk)
    solved_count = words.filter(solved=True).count()
    context = {
        'words_list': words, 
        'hsk': hsk, 
        'full_test': True, 
        'total_count': words.count(), 
        'solved_count': solved_count,
    }
    return render(request, 'test.html', context)

def check(request):
    correct = 0
    for pinyin, word_id in zip(request.POST.getlist('pinyin'), request.POST.getlist('word_id')):
        w = Word.objects.get(id=int(word_id))
        if unidecode.unidecode(w.pinyin).replace(' ', '').lower() == pinyin:
            w.solved = True
            w.save()
            correct += 1

    full_test = request.POST.get('full_test')
    if full_test == 'True':
        return HttpResponseRedirect(reverse('chinesetest:test', args=(w.hsk,)))
    else:
        return HttpResponseRedirect(reverse('chinesetest:random', args=(w.hsk,)))


def reset(request, hsk):
    Word.objects.all().filter(hsk=hsk).update(solved=False)

    return HttpResponseRedirect(reverse('chinesetest:test', args=(hsk,)))

def random(request, hsk):
    words = Word.objects.filter(hsk=hsk)
    unsolved_words = Word.objects.all().filter(hsk=hsk).filter(solved=False).order_by('?')
    if not unsolved_words:
        context = {'words_list': words, 'hsk': hsk, 'full_test':True}
    else:
        solved_count = words.count() - unsolved_words.count()
        word = unsolved_words[0]
        context = {
            'words_list': [word], 
            'hsk': hsk, 
            'full_test': False, 
            'total_count': words.count(), 
            'solved_count': solved_count,
        }

    return render(request, 'test.html', context)

def signup(request):
    if request.method == 'GET':
        print('GET')
    elif request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        if password == request.POST.get('password_repeat'):
            if User.objects.filter(username = username).first():
                print('username already exists')
            else:
                user = User.objects.create_user(username=username, password=password)

    return render(request, 'signup.html', {})

def signin(request):
    context = {}
    if request.method == 'GET':
        print('GET')
    elif request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            context['login_msg'] = 'login success'
            return HttpResponseRedirect(reverse('chinesetest:index'))
        else:
            context['login_msg'] = 'login error'
            return render(request, 'signin.html', context)

    return render(request, 'signin.html', context)

def signout(request):
    logout(request)
    return HttpResponseRedirect(reverse('chinesetest:index'))