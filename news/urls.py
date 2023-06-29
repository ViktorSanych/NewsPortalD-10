from django.urls import path

from news.views import PostDetailView, PostUpdateView, PostDeleteView, PostsListView, SearchView,\
    NewsCreateView, ArticleCreateView, ProfileUpdateView, subscribe_view

urlpatterns = [
    path('', PostsListView.as_view(), name='posts_list'),
    path('news/', PostsListView.as_view(), name='posts_list'),
    path('news/<int:pk>/', PostDetailView.as_view(), name='post_detail'),
    path('news/<int:pk>/edit/', PostUpdateView.as_view(), name='post_update'),
    path('news/<int:pk>/delete/', PostDeleteView.as_view(), name='post_delete'),
    path('news/search/', SearchView.as_view(), name='search'),
    path('news/news_create/', NewsCreateView.as_view(), name='news_create'),
    path('news/article_create/', ArticleCreateView.as_view(), name='article_create'),
    path('news/<int:pk>/profile_update/', ProfileUpdateView.as_view(), name='profile_update'),
    path('news/<int:category_id>/subscription/<str:email>/', subscribe_view, name='subscribe')
    # ...
]