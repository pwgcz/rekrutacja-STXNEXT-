from .models import Book, Category, Author
from rest_framework import serializers


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['category_id', 'name']


class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Author
        fields = ['author_id', 'name']


class BookSerializer(serializers.ModelSerializer):
    authors = serializers.SlugRelatedField(many=True,
                                           read_only=True,
                                           slug_field='name')

    categories = serializers.SlugRelatedField(many=True,
                                              read_only=True,
                                              slug_field='name')

    class Meta:
        model = Book
        fields = ['book_id',
                  'title',
                  'authors',
                  'published_date',
                  'categories',
                  'average_rating',
                  'ratings_count',
                  'thumbnail']
