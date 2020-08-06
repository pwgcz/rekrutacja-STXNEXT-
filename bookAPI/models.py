from django.db import models
from django.utils.translation import ugettext_lazy as _


class Book(models.Model):
    book_id = models.CharField(_("id"), primary_key=True, max_length=50)

    title = models.CharField(_("title"), max_length=400)
    published_date = models.TextField(
        _("published date"), null=True, blank=True
    )
    average_rating = models.FloatField(_("average rating"), null=True, blank=True)
    ratings_count = models.IntegerField(_("rating count"), null=True, blank=True)
    thumbnail = models.CharField(_("thumbnail"), max_length=500, null=True, blank=True)

    authors = models.ManyToManyField("Author")
    categories = models.ManyToManyField("Category")

    class Meta:
        verbose_name = _("book")
        verbose_name_plural = _("books")

    def __str__(self):
        return f"id: {self.book_id}, name: {self.title}"


class Author(models.Model):
    author_id = models.AutoField(primary_key=True)

    name = models.CharField(_("name"), max_length=301, null=True, blank=True)

    class Meta:
        verbose_name = _("author")
        verbose_name_plural = _("authors")

    def __str__(self):
        return f"id: {self.author_id}, name: {self.name}"


class Category(models.Model):
    category_id = models.AutoField(primary_key=True)

    name = models.CharField(_("name"), max_length=302, null=True, blank=True)

    class Meta:
        verbose_name = _("category")
        verbose_name_plural = _("categories")

    def __str__(self):
        return f"id: {self.category_id}, name: {self.name}"
