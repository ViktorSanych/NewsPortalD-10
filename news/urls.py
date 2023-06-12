from django.urls import path

from news.views import PostDetailView, PostUpdateView, PostDeleteView, NewsListView, SearchView

urlpatterns = [
    path('news/', NewsListView.as_view(), name='news_list'),
    path('news/<int:pk>/', PostDetailView.as_view(), name='post_detail'),
    path('news/<int:pk>/edit/', PostUpdateView.as_view(), name='post_update'),
    path('news/<int:pk>/delete/', PostDeleteView.as_view(), name='post_delete'),
    path('news/search/', SearchView.as_view(), name='search'),
    # ...
]