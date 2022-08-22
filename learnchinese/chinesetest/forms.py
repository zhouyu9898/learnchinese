from django import forms

class TestForm(forms.Form):
    pinyin = forms.CharField(label='pinyin', max_length=30)