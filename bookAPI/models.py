from django.db import models
from django.utils.translation import ugettext_lazy as _


class Book(models.Model):
    book_id = models.AutoField(primary_key=True)

    title = models.CharField(_('title'), max_length=200)
    published_date = models.CharField(_('published date'), max_length=4)
    average_rating = models.DecimalField(_('average rating'), default=0)
    ratings_count = models.IntegerField(_('rating count'), default=0)
    thumbnail = models.CharField(_('thumbnail'), max_length=300)

    authors = models.ManyToManyField('Author')
    categories = models.ManyToManyField('Category')

    class Meta:
        verbose_name = _('book')
        verbose_name_plural = _('books')

    def __str__(self):
        return f'id: {self.book_id}, name: {self.title}'


class Author(models.Model):
    author_id = models.AutoField(primary_key=True)

    name = models.CharField(_('name'), max_length=200)

    class Meta:
        verbose_name = _('author')
        verbose_name_plural = _('authors')

    def __str__(self):
        return f'id: {self.author_id}, name: {self.name}'


class Category(models.Model):
    category_id = models.AutoField(primary_key=True)

    name = models.CharField(_('name'), max_length=200)

    class Meta:
        verbose_name = _('category')
        verbose_name_plural = _('categories')

    def __str__(self):
        return f'id: {self.category_id}, name: {self.name}'
