import django_filters
from django import forms

from news.models import Post


class PostFilter(django_filters.FilterSet):
    title = django_filters.CharFilter(lookup_expr='icontains', label='По названию')
    author__user__username = django_filters.CharFilter(lookup_expr='icontains', label='По имени автора')
    created_at = django_filters.DateFilter(
        field_name='created_at',
        lookup_expr='gt',
        label='Позже указанной даты',
        widget=forms.DateInput(attrs={'type': 'date'})
        )

    class Meta:
        model = Post
        fields = ['title', 'author__user__username', 'created_at']