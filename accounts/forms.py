from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from .models import PasswordRestToken, Users


class RegistForm(forms.ModelForm):
    username = forms.CharField(label='名前')
    email = forms.EmailField(label='メールアドレス')
    
    class Meta:
        model = Users
        fields = ['username', 'email']
    
    def save(self, commit=False):
        user = super().save(commit=commit)
        user.set_password('default')
        user.save()
        return user


class PasswordResetForm(forms.Form):
    password = forms.CharField(
        label='新しいパスワード',
        widget=forms.PasswordInput(
            attrs={
                'class': 'large-input',
                'placeholder': '新しいパスワード'
            }
        )
    )
    confirm_password = forms.CharField(
        label='新しいパスワード確認',
        widget=forms.PasswordInput(
            attrs={
                'class': 'large-input',
                'placeholder': '新しいパスワード(確認)'
            }
        )
    )
    
    class Meta:
        fields = ['password', 'confirm_password']

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data['password']
        confirm_password = cleaned_data['confirm_password']
        try:
            validate_password(password, user=None)
        except ValidationError as e:
            raise e
        else:
            if not password == confirm_password:
                raise forms.ValidationError('パスワードが一致しません')
            self.is_valid
    
    def save(self, token, commit=False):
        user = PasswordRestToken.objects.get_user(token)
        validate_password(self.cleaned_data['password'], user)
        user.set_password(self.cleaned_data['password'])
        user.is_active = True
        user.save()
        return user



class LoginForm(AuthenticationForm):
    username = forms.EmailField(
        label='メールアドレス',
        widget=forms.TextInput(
            attrs={
                'class': 'large-input',
                'placeholder': 'example@mail.com',
            }
        )
    )
    password = forms.CharField(
        label='パスワード', 
        widget=forms.PasswordInput(
            attrs={
                'class': 'large-input',
                'placeholder': 'your password.',
            }
        )
    )
