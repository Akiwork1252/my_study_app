import os
from django import forms
from django.core.mail import EmailMessage

from .models import InterestCategory, LearningGoal, Category


# 問い合わせフォーム
class InquiryForm(forms.Form):
    name = forms.CharField(label='名前', max_length=30)
    email = forms.EmailField(label='メールアドレス')
    title = forms.CharField(label='タイトル', max_length=30)
    message = forms.CharField(label='メッセージ', widget=forms.Textarea)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['name'].widget.attrs['class'] = 'form-control'
        self.fields['name'].widget.attrs['placeholder'] = '名前をここに入力してください。'
        self.fields['email'].widget.attrs['class'] = 'form-control'
        self.fields['email'].widget.attrs['placeholder'] = 'メールアドレスをここに入力してください。'
        self.fields['title'].widget.attrs['class'] = 'form-control'
        self.fields['title'].widget.attrs['placeholder'] = 'タイトルをここに入力してください。'
        self.fields['message'].widget.attrs['class'] = 'form-control'
        self.fields['message'].widget.attrs['placeholder'] = 'メッセージをここに入力してください。'


    def send_email(self):
        name = self.cleaned_data['name']
        email = self.cleaned_data['email']
        title = self.cleaned_data['title']
        message = self.cleaned_data['message']

        subject = f'お問合せ {title}'
        message = f'送信者名: {name}\nメールアドレス: {email}'
        from_email = os.environ.get('FROM_EMAIL')
        to_list = [os.environ.get('FROM_EMAIL')]
        cc_list = [email]

        message = EmailMessage(subject=subject,
                               body=message,
                               from_email=from_email,
                               to=to_list,
                               cc=cc_list,
                               )
        message.send()


# 興味分野追加フォーム
class AddInterestCategoryForm(forms.Form):
    category = forms.ModelChoiceField(
        queryset=Category.objects.all(),
        empty_label="追加する興味分野を選択してください。",
        widget=forms.Select(attrs={'class': 'form-select'}),
    )


# 学習目標入力フォーム
class CreateLearningGoalForm(forms.ModelForm):
    class Meta:
        model = LearningGoal
        fields = ("title", "current_level", "description")
        labels = {
            'title': 'テーマ(必須)',
            'current_level': '学習経験',
            'description': '説明',
        }
        widgets = {
            'title': forms.Textarea(attrs={
                'rows': 1,
                'class': 'form-control',
                'placeholder': '学習テーマをここに入力してください。(例:Python)'
            }),
            'current_level': forms.Textarea(attrs={
                'rows': 2,
                'class': 'form-control',
                'placeholder': '経験の有無や期間を入力することで、より最適な学習プランを作成できます。(例:未経験)'
            }),
            'description': forms.Textarea(attrs={
                'rows': 6,
                'class': 'form-control',
                'placeholder': '目的や目標レベルなどの説明を追加することで、より最適な学習プランを作成できます。(例:株価予測がしたい。)'
            })
        }
