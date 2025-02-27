from django.urls import path, include
from rest_framework import routers

from book.views import (
    BookViewSet,
    AuthorViewSet
)


router = routers.DefaultRouter()
router.register("books", BookViewSet)
router.register("authors", AuthorViewSet)

urlpatterns = [path("", include(router.urls))]

app_name = "book"
