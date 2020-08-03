from .models import Book, Category, Author
from rest_framework import serializers


class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = ['book_id',
                  'title',
                  'published_date',
                  'average_rating',
                  'ratings_count',
                  'thumbnail',
                  'authors',
                  'categories']


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['category_id', 'name']


class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Author
        fields = ['author_id', 'name']
