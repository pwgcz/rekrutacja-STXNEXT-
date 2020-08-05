from json import JSONDecodeError

import requests
import os

from bookAPI.client import Client

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'books.settings')

import django

django.setup()

from bookAPI.models import Book, Category, Author
from bookAPI.serializers import BookSerializer


class BookDataIterator:
    def __init__(self, data):
        self._data = data

    def authors(self) -> list:
        authors = []
        for book in self._data['items']:
            for author in book['volumeInfo']['authors']:
                authors.append(dict(name=author))
            return author

    def categories(self) -> list:
        categories = []
        for book in self._data['items']['volumeInfo']:
            if 'categories' in book.keys():
                for category in book['categories']:
                    categories.append(dict(name=category))
                return categories

    def books(self) -> list:
        books = []
        for book in self._data['items']['volumeInfo']:
            new_book = dict(
                title=book['title'],
                authors=book['authors'],
                published_date=book['published_date'],
                thumbnail=book['imageLinks']['thumbnail'],
            )
            if 'averageRating' in book.keys():
                new_book.average_rating = book['averageRating']

            if 'ratingsCount' in book.keys():
                new_book.ratings_count = book['ratingsCount']
            books.append(new_book)
        return books

    def authors_by_book(self, book) -> list:
        pass

    def categories_by_book(self, book) -> list:
        pass


# def get_data():
#     pass


def load_to_db(data):

    iterator = BookDataIterator(data)

    for category_data in iterator.categories():
        Category.objects.create(**category_data)

    for author_data in iterator.authors():
        Author.objects.create(**author_data)

    books = []
    for book_data in iterator.books():
        book = Book(**book_data)
        for author in iterator.authors_by_book(book):
            book.authors.add(author)
        for category in iterator.categories_by_book(book):
            book.categories.add(category)
        books.append(book)
        book.save()

    return BookSerializer(books, many=True)


# def load_to_db(query: str):
#     try:
#         book_data = requests.get('https://www.googleapis.com/books/v1/volumes?q={}'.format(query)).json()
#     except JSONDecodeError:
#         return {'Error': 'Bad Request', 'status': 400}, None
#
#     all_books = []
#     for book in book_data['items']:
#         new_book = Book(book_id=book['id'],
#                         title=book['volumeInfo']['title'],
#                         published_date=book['volumeInfo']['publishedDate'],
#                         thumbnail=book['volumeInfo']['imageLinks']['thumbnail']
#                         )
#
#         if 'averageRating' in book['volumeInfo'].keys():
#             new_book.average_rating = book['volumeInfo']['averageRating']
#
#         if 'ratingsCount' in book['volumeInfo'].keys():
#             new_book.ratings_count = book['volumeInfo']['ratingsCount']
#
#         new_book.save()
#
#         for author in book['volumeInfo']['authors']:
#             if Author.objects.filter(name=author).first():
#                 new_book.authors.add(Author.objects.get(name=author))
#             else:
#                 new_author = Author(name=author)
#                 new_author.save()
#                 new_book.authors.add(new_author)
#         if 'categories' in book['volumeInfo'].keys():
#             for category in book['volumeInfo']['categories']:
#                 if Category.objects.filter(name=category).first():
#                     new_book.categories.add(Category.objects.get(name=category))
#                 else:
#                     new_category = Category(name=category)
#                     new_category.save()
#                     new_book.categories.add(new_category)
#         new_book.save()
#         serializer = BookSerializer(new_book)
#         all_books.append(serializer.data)
#
#     return all_books


if __name__ == '__main__':
    raw_data = Client('https://www.googleapis.com/books/v1/volumes').get_books('Hobbit')
    load_to_db(raw_data)
