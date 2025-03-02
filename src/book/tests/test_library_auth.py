from django.urls import reverse
from rest_framework import status

from book.tests.base_setup import BaseSetUpForTest


class BookAuthTests(BaseSetUpForTest):
    def test_non_staff_user_create_book(self):
        self.client.force_authenticate(user=self.user)

        payload = {
            "title": "New Book",
            "cover": "HARD",
            "inventory": 5,
            "daily_fee": "10.99",
            "authors": [self.author.id],
        }

        res = self.client.post(reverse("book:book-list"), payload)
        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)

    def test_non_staff_user_update_book(self):
        self.client.force_authenticate(user=self.user)

        payload = {"title": "Updated Title"}

        res = self.client.patch(
            reverse("book:book-detail", args=[self.book.id]), payload
        )
        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)

    def test_non_staff_user_delete_book(self):
        self.client.force_authenticate(user=self.user)

        response = self.client.delete(reverse("book:book-detail", args=[self.book.id]))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_non_staff_user_read_book(self):
        self.client.force_authenticate(user=self.user)

        res = self.client.get(reverse("book:book-detail", args=[self.book.id]))
        self.assertEqual(res.status_code, status.HTTP_200_OK)


class AuthorAuthTests(BaseSetUpForTest):
    def test_non_staff_user_create_author(self):
        self.client.force_authenticate(user=self.user)

        payload = {"first_name": "Unauthorized", "last_name": "Author"}

        res = self.client.post(reverse("book:author-list"), payload)
        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)

    def test_non_staff_user_update_author(self):
        self.client.force_authenticate(user=self.user)

        payload = {"first_name": "Updated Name"}

        res = self.client.patch(
            reverse("book:author-detail", args=[self.author.id]), payload
        )
        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)

    def test_non_staff_user_delete_author(self):
        self.client.force_authenticate(user=self.user)

        response = self.client.delete(
            reverse("book:author-detail", args=[self.author.id])
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_non_staff_user_read_author(self):
        self.client.force_authenticate(user=self.user)

        res = self.client.get(reverse("book:author-detail", args=[self.author.id]))
        self.assertEqual(res.status_code, status.HTTP_200_OK)
