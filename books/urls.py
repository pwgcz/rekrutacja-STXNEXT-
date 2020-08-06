from django.contrib import admin
from django.urls import path, include
from rest_framework.urlpatterns import format_suffix_patterns

from bookAPI import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api-auth/', include('rest_framework.urls')),

    path('api/', views.api_root),

    path('books', views.BookList.as_view(), name='books-list'),
    path('books/<str:pk>', views.BookDetails.as_view(), name='book-detail'),
    path('db', views.DB.as_view(), name='db'),
]

urlpatterns = format_suffix_patterns(urlpatterns)
