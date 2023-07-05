from django import forms
from .models import Post, Subscription
from django.contrib.auth.forms import UserChangeForm
from django.contrib.auth.models import User, Group


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['author', 'category', 'title', 'text']


class ProfileUpdateForm(UserChangeForm):
    email = forms.EmailField(required=True)
    group = forms.ModelChoiceField(queryset=Group.objects.all(), required=False)
    become_author = forms.BooleanField(label='Стать автором!', required=False)

    class Meta:
        model = User
        fields = ['username', 'email', 'group']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['group'].queryset = self.instance.groups.all()

    def get_user_group(self):
        user = self.instance
        if user.groups.filter(name='common').exists():
            return 'common'
        elif user.groups.filter(name='authors').exists():
            return 'authors'
        return '---'

    def save(self, commit=True):
        user = super().save(commit=False)
        if self.cleaned_data['become_author']:
            author_group, _ = Group.objects.get_or_create(name='authors')
            user.groups.add(author_group)

        if commit:
            user.save()
        return user


class SubscribeForm(forms.ModelForm):
    email = forms.EmailField(label='Email')

    def __init__(self, *args, **kwargs):
        user_email = kwargs.pop('user_email', None)
        super(SubscribeForm, self).__init__(*args, **kwargs)
        if user_email:
            self.fields['email'].initial = user_email

    class Meta:
        model = Subscription
        fields = ['category', 'email']