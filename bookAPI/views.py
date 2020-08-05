import operator
from functools import reduce

from rest_framework.decorators import api_view
from rest_framework.generics import ListAPIView, get_object_or_404
from rest_framework.reverse import reverse

from .client import Client
from .load_data import load_to_db
from .models import Book
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, filters
from .serializers import BookSerializer
from django.db.models import Q


class DB(APIView):
    def post(self, request, format=None):
        raw_data = Client("https://www.googleapis.com/books/v1/volumes").get_books(request.data['q'])
        data = load_to_db(raw_data)
        return Response(data, status=status.HTTP_201_CREATED)


class BookList(ListAPIView):

    serializer_class = BookSerializer
    filter_backends = [filters.OrderingFilter, filters.SearchFilter]

    def get_queryset(self):

        queryset = Book.objects.all()

        sort_fields = ['published_date', '-published_date']
        sort = self.request.query_params.get('sort', None)
        if sort is not None and sort in sort_fields:
            queryset = queryset.order_by(sort)

        published_date = self.request.query_params.get('published_date', None)
        if published_date is not None:
            queryset = queryset.filter(published_date=published_date)

        authors = [Q(authors__name=author) for author in self.request.query_params.getlist('author', [])]
        if authors:
            queryset = queryset.filter(reduce(operator.or_, authors))

        return queryset


class BookDetails(APIView):

    def get(self, request, pk, format=None):
        book = get_object_or_404(Book, pk=pk)
        serializer = BookSerializer(book)
        return Response(serializer.data)


@api_view(['GET'])
def api_root(request, format=None):
    return Response({
        'db': reverse('db', request=request, format=format),
        'books': reverse('books-list', request=request, format=format),
        'books/{pk}': reverse('book-detail', kwargs={'pk': 'DqLPAAAAMAAJ'}, request=request, format=format)
    })
