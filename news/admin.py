from django.contrib import admin
from .models import Author, Category, Post, PostCategory, Comment, Subscription


@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    pass


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    pass


class PostCategoryInline(admin.TabularInline):
    model = PostCategory


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    pass
    inlines = [
        PostCategoryInline,
    ]


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    pass


@admin.register(Subscription)
class SubscriptionAdmin(admin.ModelAdmin):
    pass