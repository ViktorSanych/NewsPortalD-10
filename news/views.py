from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.generic import DetailView, UpdateView, DeleteView, ListView, CreateView
from django_filters.views import FilterView
from django.urls import reverse_lazy

from .forms import PostForm, ProfileUpdateForm
from .models import Post
from .filters import PostFilter


class PostsListView(ListView):
    model = Post
    template_name = 'news/posts_list.html'
    context_object_name = 'posts'
    ordering = ['-created_at']
    paginate_by = 5


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
    success_url = reverse_lazy('posts_list')


# Представление для подтверждения удаления поста
class PostDeleteView(DeleteView):
    model = Post
    template_name = 'news/post_delete.html'
    success_url = reverse_lazy('posts_list')


# Представление для поиска статей
class SearchView(FilterView):
    model = Post
    filterset_class = PostFilter
    template_name = 'news/search.html'
    paginate_by = 3


# Представление для создания новости
class NewsCreateView(CreateView):
    form_class = PostForm
    model = Post
    template_name = 'news/news_create.html'
    success_url = reverse_lazy('posts_list')

    def form_valid(self, form):
        form.instance.post_type = Post.NEWS    # задание по умолчанию типа поста
        return super().form_valid(form)


# class NewsUpdateView(UpdateView):
#     form_class = PostForm
#     model = Post
#     template_name = 'news/post_update.html'
#
#
# class NewsDeleteView(DeleteView):
#     model = Post
#     template_name = 'news/post_delete.html'
#     success_url = reverse_lazy('posts_list')


# Представление для создания статьи
class ArticleCreateView(CreateView):
    form_class = PostForm
    model = Post
    template_name = 'news/article_create.html'
    success_url = reverse_lazy('posts_list')

    def form_valid(self, form):
        form.instance.post_type = Post.ARTICLE
        return super().form_valid(form)


# class ArticleUpdateView(UpdateView):
#     form_class = PostForm
#     model = Post
#     template_name = 'news/post_update.html'
#
#
# class ArticleDeleteView(DeleteView):
#     model = Post
#     template_name = 'news/post_delete.html'
#     success_url = reverse_lazy('posts_list')


@method_decorator(login_required, name='dispatch')
class ProfileUpdateView(UpdateView):
    model = User
    form_class = ProfileUpdateForm
    template_name = 'news/profile_update.html'
    success_url = reverse_lazy('posts_list')

    def get_object(self, queryset=None):
        return self.request.user

