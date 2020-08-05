import operator
from functools import reduce

from rest_framework.decorators import api_view
from rest_framework.generics import ListAPIView
from rest_framework.reverse import reverse

from .load_data import load_to_db
from .models import Book
from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, filters
from .serializers import BookSerializer
from django.db.models import Q


class DB(APIView):
    def post(self, request, format=None):
        data = load_to_db(request.data['q'])
        if data[1] is None:
            return Response(data[0], status=status.HTTP_400_BAD_REQUEST)
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

        authors = [Q(authors__name=author) for author in self.request.query_params.getlist('author', None)]
        if len(authors) > 0:
            queryset = queryset.filter(reduce(operator.or_, authors))

        return queryset


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
    })
