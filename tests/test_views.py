import pytest
from chat.models import Message
from django.urls import reverse_lazy
from model_bakery import baker

VIEW_URL = reverse_lazy("admin:send-banner-message")


@pytest.mark.django_db
def test_requires_login(client):
    response = client.get(VIEW_URL)
    assert response.status_code == 302


@pytest.mark.django_db
def test_requires_superuser_negative_case(client):
    user = baker.make("users.User", is_superuser=False)
    client.force_login(user)
    response = client.get(VIEW_URL)
    assert response.status_code == 302


@pytest.mark.django_db
def test_requires_superuser_positive_case(client):
    user = baker.make("users.User", is_superuser=True)
    client.force_login(user)
    response = client.get(VIEW_URL)
    assert response.status_code == 200
    assert response.context["form"]


@pytest.mark.django_db
def test_post_empty_form(client):
    user = baker.make("users.User", is_superuser=True)
    client.force_login(user)
    response = client.post(VIEW_URL)
    assert response.status_code == 200
    assert response.context["form"]
    assert not response.context["form"].is_valid()
    assert "text" in response.context["form"].errors


@pytest.mark.django_db
def test_post_valid_form(client, requests_mock):
    requests_mock.get(
        "https://api.slingacademy.com/v1/sample-data/photos/1",
        json={
            "success": True,
            "photo": {
                "url": "https://example.com/1.jpeg",
                "id": 1,
            },
        },
    )
    requests_mock.get(
        "https://example.com/1.jpeg",
        content=b"TEST",
        headers={"Content-Type": "image/jpeg"},
    )

    user = baker.make("users.User", is_superuser=True)
    baker.make("users.User")

    client.force_login(user)
    response = client.post(VIEW_URL, data={"text": "My message"})
    assert response.status_code == 302

    assert Message.objects.count() == 1
    message = Message.objects.first()
    assert message.image.external_id == 1
    assert message.text == "My message"
