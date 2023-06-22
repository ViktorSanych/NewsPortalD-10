from django import forms
from .models import Post
from django.contrib.auth.forms import UserChangeForm
from django.contrib.auth.models import User, Group


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['author', 'category', 'title', 'text']


class ProfileUpdateForm(UserChangeForm):
    email = forms.EmailField(required=True)
    group = forms.CharField(required=False, disabled=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'group']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['group'].initial = self.get_user_group()

    def get_user_group(self):
        user = self.instance
        if user.groups.filter(name='common').exists():
            return 'common'
        elif user.groups.filter(name='authors').exists():
            return 'authors'
        return '---'
