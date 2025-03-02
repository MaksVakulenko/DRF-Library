from django.test import TestCase
from django.urls import reverse
from rest_framework import status

from book.models import Book
from book.tests.base_setup import BaseSetUpForTest


class BookCRUDTests(BaseSetUpForTest):
    def test_create_book(self):
        payload = {
            "title": "New Book",
            "cover": "HARD",
            "inventory": 5,
            "daily_fee": "10.99",
            "authors": [self.author.id],
        }

        res = self.client.post(reverse("book:book-list"), payload)
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)

    def test_update_book(self):
        payload = {"title": "Updated Title"}

        res = self.client.patch(
            reverse("book:book-detail", args=[self.book.id]), payload
        )
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.book.refresh_from_db()
        self.assertEqual(self.book.title, payload["title"])

    def test_delete_book(self):
        book = Book.objects.create(
            title="Temp Book", cover=Book.CoverType.HARD, inventory=5, daily_fee=10.00
        )

        response = self.client.delete(reverse("book:book-detail", args=[book.id]))

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Book.objects.filter(id=book.id).exists())

    def test_list_books(self):
        Book.objects.create(
            title="Book 1", cover=Book.CoverType.HARD, inventory=5, daily_fee=10.00
        )
        Book.objects.create(
            title="Book 2", cover=Book.CoverType.SOFT, inventory=3, daily_fee=15.00
        )

        response = self.client.get(reverse("book:book-list"))

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        books_count = Book.objects.count()
        self.assertEqual(len(response.data), books_count)

        titles = [book["title"] for book in response.data]
        self.assertIn("Book 1", titles)
        self.assertIn("Book 2", titles)


class BookInvalidTests(BaseSetUpForTest):
    def test_create_book_invalid_data(self):
        invalid_payload = {
            "title": "",
            "cover": "INVALID",
            "inventory": -1,
            "daily_fee": "abc",
            "authors": [],
        }

        res = self.client.post(reverse("book:book-list"), invalid_payload)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_update_book_invalid_data(self):
        invalid_payload = {"title": ""}

        res = self.client.patch(
            reverse("book:book-detail", args=[self.book.id]), invalid_payload
        )
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
