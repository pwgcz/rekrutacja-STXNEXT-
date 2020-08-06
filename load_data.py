import os


os.environ.setdefault("DJANGO_SETTINGS_MODULE", "books.settings")

import django

django.setup()

from bookAPI.models import Book, Category, Author
from bookAPI.serializers import BookSerializer
from bookAPI.client import Client

class BookDataIterator:
    def __init__(self, data):
        self._data = data

    def authors(self) -> list:
        all_authors = []
        for book in self._data["items"]:
            for author in book["volumeInfo"]["authors"]:
                all_authors.append(author)

        all_authors = [dict(name=author) for author in list(set(all_authors))]
        return all_authors

    def categories(self) -> list:
        all_categories = []
        for book in self._data["items"]:
            if "categories" in book["volumeInfo"].keys():
                for category in book["volumeInfo"]["categories"]:
                    all_categories.append(category)

        all_categories = [dict(name=category) for category in list(set(all_categories))]
        return all_categories

    def books(self) -> list:
        all_books = []
        for book in self._data["items"]:
            new_book = dict(
                book_id=book["id"],
                title=book["volumeInfo"]["title"],
                published_date=book["volumeInfo"]["publishedDate"],
                thumbnail=book["volumeInfo"]["imageLinks"]["thumbnail"],
            )

            if "averageRating" in book["volumeInfo"].keys():
                new_book["average_rating"] = book["volumeInfo"]["averageRating"]

            if "ratingsCount" in book["volumeInfo"].keys():
                new_book["ratings_count"] = book["volumeInfo"]["ratingsCount"]
            all_books.append(new_book)
        return all_books

    def authors_by_book(self, selected_book) -> list:
        for book in self._data["items"]:
            if book["id"] == selected_book["book_id"]:
                return book["volumeInfo"]["authors"]
        return []

    def categories_by_book(self, selected_book) -> list:
        for book in self._data["items"]:
            if book["id"] == selected_book["book_id"]:
                if "categories" in book["volumeInfo"].keys():
                    return book["volumeInfo"]["categories"]
        return []


def load_to_db(data):
    iterator = BookDataIterator(data)

    all_categories_in_db = [category.name for category in Category.objects.all()]
    for category_data in iterator.categories():
        if not category_data["name"] in all_categories_in_db:
            Category.objects.create(**category_data)

    all_authors_in_db = [author.name for author in Author.objects.all()]
    for author_data in iterator.authors():
        if not author_data["name"] in all_authors_in_db:
            Author.objects.create(**author_data)
    books = []
    for book_data in iterator.books():
        book = Book(**book_data)
        book.save()
        for author in iterator.authors_by_book(book_data):
            book.authors.add(Author.objects.get(name=author))
        for category in iterator.categories_by_book(book_data):
            book.categories.add(Category.objects.get(name=category))

        books.append(book)
        book.save()

    return BookSerializer(books, many=True)


if __name__ == "__main__":
    raw_data = Client("https://www.googleapis.com/books/v1/volumes").get_books("Hobbit")
    load_to_db(raw_data)
