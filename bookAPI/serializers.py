from .models import Book, Category, Author
from rest_framework import serializers


class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = []


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = []


class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Author
        fields = []
