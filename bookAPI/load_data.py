import requests
import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'books.settings')

import django
django.setup()

from bookAPI.models import Book, Category, Author


def load_to_db():
    book_data = requests.get('https://www.googleapis.com/books/v1/volumes?q=Hobbit').json()

    for book in book_data['items']:

        new_book = Book(book_id=book['id'],
                        title=book['volumeInfo']['title'],
                        published_date=book['volumeInfo']['publishedDate'],
                        thumbnail=book['volumeInfo']['imageLinks']['thumbnail']
                        )

        if 'averageRating' in book['volumeInfo'].keys():
            new_book.average_rating = book['volumeInfo']['averageRating']

        if 'ratingsCount' in book['volumeInfo'].keys():
            new_book.ratings_count = book['volumeInfo']['ratingsCount']

        new_book.save()

        for author in book['volumeInfo']['authors']:
            if Author.objects.filter(name=author).first():
                new_book.authors.add(Author.objects.get(name=author))
            else:
                new_author = Author(name=author)
                new_author.save()
                new_book.authors.add(new_author)
        if 'categories' in book['volumeInfo'].keys():
            for category in book['volumeInfo']['categories']:
                if Category.objects.filter(name=category).first():
                    new_book.categories.add(Category.objects.get(name=category))
                else:
                    new_category = Category(name=category)
                    new_category.save()
                    new_book.categories.add(new_category)

        new_book.save()


if __name__ == '__main__':
    load_to_db()
