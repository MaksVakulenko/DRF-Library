from rest_framework import (
    viewsets,
    filters,
    permissions
)
from rest_framework_simplejwt.authentication import JWTAuthentication

from book.models import (
    Book,
    Author
)

from book.serializers import (
    BookSerializer,
    AuthorSerializer
)


class BaseViewSet(viewsets.ModelViewSet):
    authentication_classes = [JWTAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [
        filters.SearchFilter,
        filters.OrderingFilter
    ]


class BookViewSet(BaseViewSet):
    queryset = Book.objects.prefetch_related("actors")
    serializer_class = BookSerializer
    search_fields = [
        "title",
        "authors",
        "cover",
        "daily_fee"
    ]
    ordering_fields = [
        "id",
        "authors",
        "title"
    ]


class AuthorViewSet(BaseViewSet):
    queryset = Author.objects.prefetch_related("books")
    serializer_class = AuthorSerializer
