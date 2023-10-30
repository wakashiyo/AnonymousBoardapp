from django import forms
from .models import Comment
from django.core.validators import RegexValidator
from django.forms.widgets import ClearableFileInput
import re

class CommentForm(forms.ModelForm):
    password = forms.CharField(
    widget=forms.PasswordInput(attrs={
        'placeholder': 'パスワードを入力（任意/6桁以下の数字）',
        'style': 'width: 350px;',
    }),
    label='パスワード',
    required=False
)

    class Meta:
        model = Comment
        fields = ('body', 'password',)
        widgets = {
            'body': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': '質問の内容を入力してください。',
                'rows': '10'
            }),
        }
        labels = {
            'body': '',
            'password': 'パスワード：',
        }

    def clean(self):
        data = super().clean()
        body = data.get('body')
        if body is None:
            msg = "本文が入力されていません"
            self.add_error('body', msg)
        elif len(body) > 1000:
            msg = "本文の最大文字数は1000文字です"
            self.add_error('body', msg)
        
    def clean_password(self):
        password = self.cleaned_data.get('password')
        if password and not re.match(r'^\d{1,6}$', password):
            raise forms.ValidationError('6桁以下の数字を入力してください。')

        return password