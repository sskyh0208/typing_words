from django import forms
from django.forms.widgets import TextInput
from .models import WordBooks, Words


class WordBooksForm(forms.ModelForm):
    name = forms.CharField(
        label='単語帳名',
        widget=forms.TextInput(
            attrs={
                'class': 'large-input',
                'placeholder': '単語帳名',
                'autocomplete': 'off'
            }
        )
    )
    description = forms.CharField(
        label='説明',
        widget=forms.TextInput(
            attrs={
                'class': 'large-input',
                'placeholder': '説明',
                'autocomplete': 'off'
            }
        )
    )
    publish = forms.BooleanField(label='公開する', required=False)

    class Meta:
        model = WordBooks
        fields = ['name', 'description', 'publish']

    def save(self):
        workbook = super().save(commit=False)
        # ここで参照関係のユーザを渡す
        workbook.user = self.user
        workbook.save()
        return workbook

    
class WordsForm(forms.ModelForm):
    name = forms.CharField(
        label='単語',
        widget=forms.TextInput(
            attrs={
                'class': 'large-input',
                'placeholder': '単語',
                'autocomplete': 'off'
            }
        )
    )
    description = forms.CharField(
        label='意味',
        widget=forms.TextInput(
            attrs={
                'class': 'large-input',
                'placeholder': '意味',
                'autocomplete': 'off'
            }
        )
    )

    class Meta:
        model = Words
        fields = ['name', 'description']

    def save(self):
        word = super().save(commit=False)
        word.wordbook = self.wordbook
        word.save()
        return word