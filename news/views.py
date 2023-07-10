from django.contrib.auth.models import User, Group
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.shortcuts import redirect, render, get_object_or_404
from django.utils.decorators import method_decorator
from django.views.generic import DetailView, UpdateView, DeleteView, ListView, CreateView
from django_filters.views import FilterView
from django.urls import reverse_lazy

from .forms import PostForm, ProfileUpdateForm, SubscribeForm
from .models import Post, Category, Subscription
from .filters import PostFilter
from .utils.mails import send_subscribe_mail


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

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['email'] = self.request.GET.get('email')  # Получаем значение параметра 'email' из запроса
        return context


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
class NewsCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    form_class = PostForm
    model = Post
    template_name = 'news/news_create.html'
    success_url = reverse_lazy('posts_list')
    permission_required = 'news.news_create'

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
class ArticleCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    form_class = PostForm
    model = Post
    template_name = 'news/article_create.html'
    success_url = reverse_lazy('posts_list')
    permission_required = 'news.article_create'

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

    def form_valid(self, form):
        if form.cleaned_data['become_author']:
            author_group, _ = Group.objects.get_or_create(name='authors')
            self.request.user.groups.add(author_group)
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        subscriptions = Subscription.objects.filter(user=user)
        context['subscriptions'] = subscriptions
        return context


@login_required
def subscribe_view(request, category_id):
    category = get_object_or_404(Category, id=category_id)
    user_email = request.user.email
    user = request.user

    if request.method == 'POST':
        form = SubscribeForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']

            # Создаем подписку
            subscription = Subscription(email=email, category=category, user_id=user.id)
            subscription.save()

            # Отправляем письмо подписчику
            send_subscribe_mail(email, category.name_category)

            # Переход на страницу со списком новостей
            return redirect('posts_list')
    else:
        form = SubscribeForm(user_email=user_email)

    return render(request, 'news/subscription.html', {'form': form, 'category': category, 'email': user_email})