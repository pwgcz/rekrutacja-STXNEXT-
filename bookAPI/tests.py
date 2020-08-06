import json

from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from bookAPI.client import Client
from load_data import load_to_db


class BookTests(APITestCase):
    def setUp(self):
        raw_data = Client("https://www.googleapis.com/books/v1/volumes").get_books(
            "Hobbit"
        )
        load_to_db(raw_data)

    def test_add_to_database(self):
        url = reverse("db")
        data = {"q": "war"}
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_book_list(self):
        response = self.client.get(reverse("books-list"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_book_detail(self):
        response = self.client.get(
            reverse("book-detail", kwargs={"pk": "YyXoAAAACAAJ"})
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 7)
        self.assertEqual(
            response.data,
            {
                "title": "Hobbit czyli Tam i z powrotem",
                "authors": ["J. R. R. Tolkien"],
                "published_date": "2004",
                "categories": ["Baggins, Bilbo (Fictitious character)"],
                "average_rating": 5,
                "ratings_count": 2,
                "thumbnail": "http://books.google.com/books/content?id=YyXoAAAACAAJ&printsec=frontcover&img=1&zoom=1&source=gbs_api",
            },
        )

    def test_filter_by_published_year(self):
        response = self.client.get("/books?published_date=1995", format="json")

        for date in json.loads(response.content):
            self.assertEqual(date["published_date"], "1995")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_sorting_by_ascending_published_year(self):
        response = self.client.get("/books?sort=published_date", format="json")
        date_list = [date["published_date"] for date in json.loads(response.content)]

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(date_list, sorted(date_list))

    def test_sorting_by_descending_published_year(self):
        response = self.client.get("/books?sort=-published_date", format="json")
        date_list = [date["published_date"] for date in json.loads(response.content)]

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(date_list, sorted(date_list, reverse=True))

    def test_filtering_by_author(self):
        response = self.client.get("/books?author=J. R. R. Tolkien", format="json")

        for authors in json.loads(response.content):
            for author in authors["authors"]:
                self.assertEqual(author, "J. R. R. Tolkien")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_filtering_by_many_authors(self):
        response = self.client.get(
            "/books?author=J. R. R. Tolkien&author=Ed Strauss", format="json"
        )

        all_author = []
        for authors in json.loads(response.content):
            for author in authors["authors"]:
                all_author.append(author)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("J. R. R. Tolkien", all_author)
        self.assertIn("Ed Strauss", all_author)
