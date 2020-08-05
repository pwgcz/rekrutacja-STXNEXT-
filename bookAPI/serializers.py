from .models import Book
from rest_framework import serializers


class BookSerializer(serializers.ModelSerializer):
    authors = serializers.SlugRelatedField(many=True,
                                           read_only=True,
                                           slug_field='name')

    categories = serializers.SlugRelatedField(many=True,
                                              read_only=True,
                                              slug_field='name')

    class Meta:
        model = Book
        fields = ['title',
                  'authors',
                  'published_date',
                  'categories',
                  'average_rating',
                  'ratings_count',
                  'thumbnail']
