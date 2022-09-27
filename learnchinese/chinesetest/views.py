from django.shortcuts import render, reverse
from django.http import HttpResponse, HttpResponseRedirect
from django.db.models.query import EmptyQuerySet
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from .models import Word, Solve
from .forms import TestForm
import random
import unidecode


def index(request):
    hsks = [i for i in range(1,7)]
    solved_counts = []
    total_counts = []
    if request.user.is_authenticated:    
        for hsk in hsks:
            words = Word.objects.filter(hsk=hsk)
            solved_words = Solve.objects.filter(user=request.user).filter(word__hsk=hsk)
            solved_counts.append(solved_words.count())
            total_counts.append(words.count())

    else:
        if not request.session.has_key('solved_words'):
            request.session['solved_words'] = {str(i): [] for i in range(1,7)}
        solved_words_dict = request.session['solved_words']
        for hsk in hsks:
            words = Word.objects.filter(hsk=hsk)
            total_counts.append(words.count())
            solved_counts.append(len(solved_words_dict[str(hsk)]))

    context = {
        'hsks': zip(hsks, solved_counts, total_counts)
    }
    return render(request, 'index.html', context)

def test(request, hsk):
    words = Word.objects.filter(hsk=hsk)
    total_count = words.count()
    if request.user.is_authenticated:
        solved_words = Solve.objects.filter(user=request.user).filter(word__hsk=hsk)
        solved_count = solved_words.count()
        words = words.exclude(id__in=solved_words.values_list('word__id'))
    else:
        if not request.session.has_key('solved_words'):
            request.session['solved_words'] = {i: [] for i in range(1,7)}
        solved_words_id = request.session['solved_words'][str(hsk)]
        words = words.exclude(id__in=solved_words_id)
        solved_count = len(solved_words_id)

    
    context = {
        'words_list': words, 
        'hsk': hsk, 
        'full_test': True, 
        'total_count': total_count, 
        'solved_count': solved_count,
    }
    return render(request, 'test.html', context)

def check(request):
    if request.user.is_authenticated:
        for pinyin, word_id in zip(request.POST.getlist('pinyin'), request.POST.getlist('word_id')):
            w = Word.objects.get(id=int(word_id))
            if unidecode.unidecode(w.pinyin).replace(' ', '').lower() == pinyin:
                Solve.objects.create(user=request.user, word=w)
    else:
        if not request.session.has_key('solved_words'):
            request.session['solved_words'] = {i: [] for i in range(1,7)}
        for pinyin, word_id in zip(request.POST.getlist('pinyin'), request.POST.getlist('word_id')):
            w = Word.objects.get(id=int(word_id))
            if unidecode.unidecode(w.pinyin).replace(' ', '').lower() == pinyin:
                request.session['solved_words'][str(w.hsk)].append(w.id)
                request.session.modified = True

    full_test = request.POST.get('full_test')
    if full_test == 'True':
        return HttpResponseRedirect(reverse('chinesetest:test', args=(w.hsk,)))
    else:
        return HttpResponseRedirect(reverse('chinesetest:random', args=(w.hsk,)))


def reset(request, hsk):
    if request.user.is_authenticated:
        Solve.objects.filter(user=request.user).filter(word__hsk=hsk).delete()
    else:
        if not request.session.has_key('solved_words'):
            request.session['solved_words'] = {i: [] for i in range(1,7)}
        request.session['solved_words'][str(hsk)] = []
        request.session.modified = True

    return HttpResponseRedirect(reverse('chinesetest:test', args=(hsk,)))

def random(request, hsk):
    words = Word.objects.filter(hsk=hsk)
    total_count = words.count()
    full_test = True
    if request.user.is_authenticated:
        solved_words = Solve.objects.filter(user=request.user).filter(word__hsk=hsk)
        solved_count = solved_words.count()
        unsolved_words = Word.objects.filter(hsk=hsk).exclude(
                id__in=solved_words.values_list('word__id')
            ).order_by('?')
        if unsolved_words:
            full_test = False
            words = [unsolved_words[0]]
    else:
        if not request.session.has_key('solved_words'):
            request.session['solved_words'] = {i: [] for i in range(1,7)}
        solved_words_id = request.session['solved_words'][str(hsk)]
        solved_count = len(solved_words_id)
        unsolved_words = words.exclude(id__in=solved_words_id).order_by('?')
        if unsolved_words:
            full_test = False
            words = [unsolved_words[0]]

    context = {
        'words_list': words, 
        'hsk': hsk, 
        'full_test': full_test, 
        'total_count': total_count, 
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