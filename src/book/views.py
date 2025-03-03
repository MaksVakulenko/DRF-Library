from django.db.models import Prefetch, F
from drf_spectacular.utils import extend_schema
from rest_framework import viewsets, filters
from rest_framework.permissions import IsAuthenticated, IsAdminUser, AllowAny

from book.models import Book, Author

from book.serializers import (
    BookSerializer,
    AuthorSerializer,
    BookListSerializer,
    BookRetrieveSerializer,
)
import library_service.examples_swagger as swagger


class BaseViewSet(viewsets.ModelViewSet):
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]

    def get_permissions(self):
        """
        All users can see list of books and authors.
        But only admins can edit list of books and authors.
        """
        if self.action in ("create", "update", "partial_update", "destroy"):
            return [IsAuthenticated(), IsAdminUser()]
        if self.action in ("list", "retrieve"):
            return [AllowAny(),]
        return [
            IsAuthenticated()
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

    @extend_schema(
        parameters=swagger.book_search_and_ordering_parameters
    )
    def list(self, request, *args, **kwargs):
        """Get list of books."""
        return super().list(request, *args, **kwargs)

    @extend_schema(
        examples=swagger.post_book_example
    )
    def create(self, request, *args, **kwargs):
        """Create new book."""
        return super().create(request, *args, **kwargs)

    @extend_schema(
        parameters=swagger.book_id_parameter
    )
    def retrieve(self, request, *args, **kwargs):
        """Get book details."""
        return super().retrieve(request, *args, **kwargs)

    @extend_schema(
        parameters=swagger.book_id_parameter,
        examples=swagger.put_book_example,
    )
    def update(self, request, *args, **kwargs):
        """Update book."""
        return super().update(request, *args, **kwargs)

    @extend_schema(
        parameters=swagger.book_id_parameter,
        examples=swagger.patch_book_example,
    )
    def partial_update(self, request, *args, **kwargs):
        """Partially update book."""
        return super().partial_update(request, *args, **kwargs)

    @extend_schema(
        parameters=swagger.book_id_parameter_delete,
    )
    def destroy(self, request, *args, **kwargs):
        """Delete book."""
        return super().destroy(request, *args, **kwargs)

class AuthorViewSet(BaseViewSet):
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer
    search_fields = ["first_name", "last_name"]
    ordering_fields = [
        "id",
        "first_name",
        "last_name",
    ]
    ordering = ["id"]

    @extend_schema(
        parameters=swagger.author_search_and_ordering_parameters
    )
    def list(self, request, *args, **kwargs):
        """Retrieve all authors."""
        return super().list(request, *args, **kwargs)

    @extend_schema(
        parameters=swagger.author_id_parameter,
    )
    def retrieve(self, request, *args, **kwargs):
        """Retrieve a single author."""
        return super().retrieve(request, *args, **kwargs)

    @extend_schema(
        examples=swagger.post_authors_example
    )
    def create(self, request, *args, **kwargs):
        """Create a new author."""
        return super().create(request, *args, **kwargs)

    @extend_schema(
        parameters=swagger.author_id_parameter,
        examples=swagger.put_author_example
    )
    def update(self, request, *args, **kwargs):
        """Update an existing author."""
        return super().update(request, *args, **kwargs)

    @extend_schema(
        parameters=swagger.author_id_parameter,
        examples=swagger.patch_author_example
    )
    def partial_update(self, request, *args, **kwargs):
        """Partially update an existing author."""
        return super().partial_update(request, *args, **kwargs)

    @extend_schema(
        parameters=swagger.author_id_parameter_to_delete
    )
    def destroy(self, request, *args, **kwargs):
        """Delete an existing author."""
        return super().destroy(request, *args, **kwargs)