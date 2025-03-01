from django.db.models import Prefetch, F
from rest_framework import viewsets, filters
from rest_framework.permissions import IsAuthenticated, IsAdminUser

from book.models import Book, Author

from book.serializers import (
    BookSerializer,
    AuthorSerializer,
    BookListSerializer,
    BookRetrieveSerializer,
)


class BaseViewSet(viewsets.ModelViewSet):
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]

    def get_permissions(self):
        if self.action in ("create", "update", "partial_update", "destroy"):
            return [IsAuthenticated(), IsAdminUser()]
        return [
            IsAuthenticated(),
        ]


class BookViewSet(BaseViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    search_fields = ["title", "authors__first_name", "authors__last_name"]
    ordering_fields = [
        "id",
        "title",
        "primary_author_first_name",
        "primary_author_last_name",
    ]
    ordering = ["id"]

    def get_queryset(self):
        authors = Author.objects.all()

        queryset = Book.objects.prefetch_related(
            Prefetch("authors", queryset=Author.objects.all())
        ).annotate(
            primary_author_first_name=F("authors__first_name"),
            primary_author_last_name=F("authors__last_name"),
        )

        return queryset

    def get_serializer_class(self):
        if self.action == "list":
            return BookListSerializer
        if self.action == "retrieve":
            return BookRetrieveSerializer
        return BookSerializer


class AuthorViewSet(BaseViewSet):
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer
