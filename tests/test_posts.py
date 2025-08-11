import pytest
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from django.contrib.auth.models import User
from api.models import Post, SubPost, View
from threading import Thread


@pytest.mark.django_db
class TestPostAPI:
    @pytest.fixture(autouse=True)
    def setup(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username="user1", password="pass")
        self.client.force_authenticate(user=self.user)
        self.post_data = {
            "title": "Test Post",
            "body": "Test Body",
            "subposts": [
                {"title": "Sub 1", "body": "Sub body 1"},
                {"title": "Sub 2", "body": "Sub body 2"},
            ],
        }

    def test_create_post_with_subposts(self):
        url = reverse("post-list")
        response = self.client.post(url, self.post_data, format="json")
        assert response.status_code == status.HTTP_201_CREATED
        assert response.data["title"] == self.post_data["title"]
        assert len(response.data["subposts"]) == 2

    def test_get_post(self):
        post = Post.objects.create(title="P1", body="B1", author=self.user)
        SubPost.objects.create(post=post, author=self.user, title="Sub1", body="Body1")
        url = reverse("post-detail", args=[post.id])
        response = self.client.get(url)
        assert response.status_code == status.HTTP_200_OK
        assert response.data["id"] == post.id
        assert "subposts" in response.data

    def test_update_post_and_subposts(self):
        post = Post.objects.create(title="Old Title", body="Old Body", author=self.user)
        sp = SubPost.objects.create(
            post=post, author=self.user, title="Old Sub", body="Old Body"
        )

        url = reverse("post-detail", args=[post.id])
        updated_data = {
            "title": "New Title",
            "body": "New Body",
            "subposts": [
                {"id": sp.id, "title": "Updated Sub", "body": "Updated Body"},
                {"title": "New Sub", "body": "New Sub Body"},
            ],
        }
        response = self.client.put(url, updated_data, format="json")
        assert response.status_code == status.HTTP_200_OK
        assert response.data["title"] == "New Title"
        assert len(response.data["subposts"]) == 2

        post.refresh_from_db()
        assert post.title == "New Title"
        assert post.subposts.count() == 2

    def test_delete_post(self):
        post = Post.objects.create(title="ToDelete", body="Body", author=self.user)
        url = reverse("post-detail", args=[post.id])
        response = self.client.delete(url)
        assert response.status_code == status.HTTP_204_NO_CONTENT
        assert not Post.objects.filter(id=post.id).exists()


@pytest.mark.django_db()
class TestPostLike:
    @pytest.fixture(autouse=True)
    def setup(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username="user", password="pass")

        self.client.force_authenticate(user=self.user)

    def test_like_post(self):
        post = Post.objects.create(title="Post_like", body="Body", author=self.user)
        url = reverse("like-post", args=[post.id])
        response = self.client.post(url)
        assert response.status_code == status.HTTP_200_OK
        response = self.client.post(url)
        assert response.status_code == status.HTTP_400_BAD_REQUEST


@pytest.mark.django_db(transaction=True)
class TestPostViewsConcurrency:
    @pytest.fixture(autouse=True)
    def setup(self):
        self.client1 = APIClient()
        self.client2 = APIClient()
        self.user1 = User.objects.create_user(username="user1", password="pass")
        self.user2 = User.objects.create_user(username="user2", password="pass")

        self.client1.force_authenticate(user=self.user1)
        self.client2.force_authenticate(user=self.user2)

        self.post = Post.objects.create(
            title="Test Post", body="Test Body", author=self.user1
        )

    def view_post(self, client, pk, results, index):
        url = reverse("view-post", args=[pk])
        response = client.post(url)
        results[index] = response.status_code

    def test_concurrent_views_increment(self):
        results = [None, None]

        t1 = Thread(
            target=self.view_post, args=(self.client1, self.post.id, results, 0)
        )
        t2 = Thread(
            target=self.view_post, args=(self.client2, self.post.id, results, 1)
        )

        t1.start()
        t2.start()
        t1.join()
        t2.join()

        assert results[0] == status.HTTP_200_OK
        assert results[1] == status.HTTP_200_OK

        self.post.refresh_from_db()
        assert self.post.views_count == 2

        assert View.objects.filter(user=self.user1, post=self.post).exists()
        assert View.objects.filter(user=self.user2, post=self.post).exists()
