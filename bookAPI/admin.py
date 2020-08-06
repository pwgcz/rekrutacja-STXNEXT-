from django.contrib import admin
from .models import Book, Category, Author


class CategoryAdmin(admin.ModelAdmin):
    empty_value_display = "unknown"
    fields = ("name",)


class AuthorAdmin(admin.ModelAdmin):
    empty_value_display = "unknown"
    fields = ("name",)


class BookAdmin(admin.ModelAdmin):
    empty_value_display = "unknown"
    fields = (
        "book_id",
        "title",
        "published_date",
        "average_rating",
        "ratings_count",
        "thumbnail",
        "authors",
        "categories",
    )


admin.site.register(Category, CategoryAdmin)
admin.site.register(Author, AuthorAdmin)
admin.site.register(Book, BookAdmin)
