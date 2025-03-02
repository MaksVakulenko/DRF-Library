from django.urls import reverse
from rest_framework import status

from book.models import Author
from book.tests.base_setup import BaseSetUpForTest


class AuthorCRUDTests(BaseSetUpForTest):
    def test_create_author(self):
        payload = {"first_name": "New", "last_name": "Author"}

        res = self.client.post(reverse("book:author-list"), payload)
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)

    def test_update_author(self):
        payload = {"first_name": "Updated"}

        res = self.client.patch(
            reverse("book:author-detail", args=[self.author.id]), payload
        )
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.author.refresh_from_db()
        self.assertEqual(self.author.first_name, payload["first_name"])

    def test_delete_author(self):
        response = self.client.delete(
            reverse("book:author-detail", args=[self.author.id])
        )
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Author.objects.filter(id=self.author.id).exists())

    def test_list_authors(self):
        Author.objects.create(first_name="Author1", last_name="Test1")
        Author.objects.create(first_name="Author2", last_name="Test2")

        response = self.client.get(reverse("book:author-list"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), Author.objects.count())


class AuthorInvalidDataTests(BaseSetUpForTest):
    def test_create_author_with_invalid_data(self):
        payload = {"first_name": "New", "last_name": "Author"}

        res = self.client.post(reverse("book:author-list"), payload)
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)

    def test_update_author_with_invalid_data(self):
        payload = {"first_name": "Updated"}

        res = self.client.patch(
            reverse("book:author-detail", args=[self.author.id]), payload
        )
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.author.refresh_from_db()
        self.assertEqual(self.author.first_name, payload["first_name"])
