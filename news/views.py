from django.views.generic import DetailView, UpdateView, DeleteView, ListView, CreateView
from django_filters.views import FilterView
from django.urls import reverse_lazy

from .forms import PostForm
from .models import Post
from news.filters import PostFilter


class PostsListView(ListView):
    model = Post
    template_name = 'news/posts_list.html'
    context_object_name = 'posts'
    ordering = ['-created_at']
    paginate_by = 3


# Представление для полного текста поста
class PostDetailView(DetailView):
    model = Post
    template_name = 'news/post_detail.html'
    context_object_name = 'post'


# Представление для редактирования поста
class PostUpdateView(UpdateView):
    model = Post
    template_name = 'news/post_update.html'
    fields = ['title', 'text']  # Указать необходимые поля для редактирования


# Представление для подтверждения удаления поста
class PostDeleteView(DeleteView):
    model = Post
    template_name = 'news/post_delete.html'
    success_url = reverse_lazy('news_list')


# Представление для поиска статей
class SearchView(FilterView):
    model = Post
    filterset_class = PostFilter
    template_name = 'news/search.html'
    paginate_by = 3


class NewsCreate(CreateView):
    form_class = PostForm
    model = Post
    template_name = 'news/post_update.html'


class NewsUpdate(UpdateView):
    form_class = PostForm
    model = Post
    template_name = 'news/post_update.html'


class NewsDelete(DeleteView):
    model = Post
    template_name = 'news/post_delete.html'
    success_url = reverse_lazy('news_list')


class ArticleCreate(CreateView):
    form_class = PostForm
    model = Post
    template_name = 'news/post_update.html'


class ArticleUpdate(UpdateView):
    form_class = PostForm
    model = Post
    template_name = 'news/post_update.html'


class ArticleDelete(DeleteView):
    model = Post
    template_name = 'news/post_delete.html'
    success_url = reverse_lazy('news_list')