from rest_framework.decorators import api_view
from rest_framework.generics import ListAPIView
from rest_framework.reverse import reverse

from .load_data import load_to_db
from .models import Book, Category, Author
from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, filters
from .serializers import BookSerializer, CategorySerializer, AuthorSerializer


class DB(APIView):
    def post(self, request, format=None):

        if load_to_db(request.data['q']) is None:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        return Response(status=status.HTTP_201_CREATED)


class BookList(ListAPIView):

    queryset = Book.objects.all()
    serializer_class = BookSerializer
    filter_backends = [filters.OrderingFilter, filters.SearchFilter]
    ordering_fields = ['published_date']
    search_fields = ['published_date']


class BookDetails(APIView):

    def get_object(self, pk):
        try:
            return Book.objects.get(pk=pk)
        except Book.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        book = self.get_object(pk)
        serializer = BookSerializer(book)
        return Response(serializer.data)


@api_view(['GET'])
def api_root(request, format=None):
    return Response({
        'db': reverse('db', request=request, format=format),
        'books': reverse('books-list', request=request, format=format),
        'books/<pk>': reverse('book-detail', kwargs={'pk': 'YyXoAAAACAAJ'}, request=request, format=format)
        # 'authors': reverse('authors', request=request, format=format),
        # 'categories': reverse('categories', request=request, format=format),
    })
