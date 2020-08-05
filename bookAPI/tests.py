import json

from rest_framework.test import APIRequestFactory

from django.urls import reverse
from rest_framework import status
from rest_framework.exceptions import ErrorDetail
from rest_framework.test import APITestCase

from bookAPI.models import Book, Category, Author
from bookAPI.views import BookDetails


class BookTests(APITestCase):

    def SetUp(self):
        self.author = Author.objects.create(name='J. R. R. Tolkien')
        self.category = Category.objects.create(name='Baggins, Bilbo (Fictitious character)')
        self.book = Book.objects.create(title='Hobbit czyli Tam i z powrotem',
                                        authors=self.author,
                                        published_date="2004",
                                        categories=self.category,
                                        average_rating=5,
                                        ratings_count=2,
                                        thumbnail="http://books.google.com/books/content?id=YyXoAAAACAAJ&printsec=frontcover&img=1&zoom=1&source=gbs_api"
                                        )

    def test_add_to_database(self):
        url = reverse('db')
        data = {'q': 'war'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_view_list(self):

        response = self.client.post('/db/', {'q': 'Hoobbit'}, format=json)

    def test_selected_book(self):
        # response = self.client.get(reverse('book-detail', kwargs={'pk': 'DqLPAAAAMAAJ'}))
        response = self.client.get(reverse('books-list'))

        print(response.data)

        # self.assertEqual(len(response.data), 1)
