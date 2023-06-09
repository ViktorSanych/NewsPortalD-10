# Generated by Django 4.2.1 on 2023-06-20 11:16

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('news', '0002_alter_author_options_alter_category_options_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='author',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='news.author', verbose_name='Автор'),
        ),
        migrations.AlterField(
            model_name='post',
            name='category',
            field=models.ManyToManyField(through='news.PostCategory', to='news.category', verbose_name='Категория'),
        ),
        migrations.AlterField(
            model_name='post',
            name='post_type',
            field=models.CharField(choices=[('article', 'Статья'), ('news', 'Новость')], max_length=10, verbose_name='тип поста'),
        ),
        migrations.AlterField(
            model_name='post',
            name='rating',
            field=models.IntegerField(default=0, verbose_name='Рейтинг'),
        ),
        migrations.AlterField(
            model_name='post',
            name='text',
            field=models.TextField(verbose_name='Содержание'),
        ),
        migrations.AlterField(
            model_name='post',
            name='title',
            field=models.CharField(max_length=200, verbose_name='Заголовок'),
        ),
        migrations.AlterField(
            model_name='postcategory',
            name='category',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='news.category', verbose_name='Категории'),
        ),
    ]
