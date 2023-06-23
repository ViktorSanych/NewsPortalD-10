from django.db import models
from django.contrib.auth.models import User, Group
from django.db.models import Sum


class Author(models.Model):
    class Meta:
        verbose_name = 'Автор'
        verbose_name_plural = 'Авторы'

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    rating_author = models.IntegerField(default=0)

    def __str__(self):
        return self.user.username

    def update_rating(self):
        post_rating = self.post_set.aggregate(total_rating=Sum('rating'))['total_rating'] or 0
        commet_rating = self.comment_set.aggregate(total_rating=Sum('rating'))['total_rating'] or 0
        post_comment_rating = self.post_set.aggregate(total_rating=Sum('comments__rating'))['total_rating'] or 0

        self.rating_author = (post_rating*3) + commet_rating + post_comment_rating


class Category(models.Model):
    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    name_category = models.CharField(max_length=150, unique=True)

    def __str__(self):
        return self.name_category


class Post(models.Model):
    class Meta:
        verbose_name = 'Пост'
        verbose_name_plural = 'Посты'

    ARTICLE = 'article'
    NEWS = 'news'
    POST_TYPES = [
        (ARTICLE, 'Статья'),
        (NEWS, 'Новость'),
    ]

    author = models.ForeignKey(Author, verbose_name='Автор', on_delete=models.CASCADE)
    post_type = models.CharField(max_length=10, verbose_name='тип поста', choices=POST_TYPES)
    created_at = models.DateTimeField(auto_now_add=True)
    category = models.ManyToManyField(Category, verbose_name='Категория', through='PostCategory')
    title = models.CharField(max_length=200, verbose_name='Заголовок')
    text = models.TextField(verbose_name='Содержание')
    rating = models.IntegerField(default=0, verbose_name='Рейтинг')

    def __str__(self):
        return self.title

    def like(self):
        self.rating += 1
        self.save()

    def dislike(self):
        self.rating += 1
        self.save()

    def preview(self):
        return self.title[:124] + '...'


class PostCategory(models.Model):
    class Meta:
        verbose_name = 'Категория поста'
        verbose_name_plural = 'Категории постов'

    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, verbose_name='Категории', on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.post.title} - {self.category.name_category}'


class Comment(models.Model):
    class Meta:
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'

    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    comment_text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    rating = models.IntegerField(default=0)

    def __str__(self):
        return f'Comment by {self.author.user.username} on {self.post.title}'

    def like(self):
        self.rating += 1
        self.save()

    def dislike(self):
        self.rating += 1
        self.save()