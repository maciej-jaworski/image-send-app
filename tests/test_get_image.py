import pytest
from chat.image_api import GetImageException, get_new_image
from chat.models import Image


@pytest.mark.django_db
def test_get_image_basic_case(requests_mock):
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

    image = get_new_image()
    assert image
    assert image.image_file


@pytest.mark.django_db
def test_get_image_when_image_already_exists(requests_mock):
    """
    Ensure that we fetch the next id in order
    """
    Image.objects.create(external_id=10)
    requests_mock.get(
        "https://api.slingacademy.com/v1/sample-data/photos/11",
        json={
            "success": True,
            "photo": {
                "url": "https://example.com/11.jpeg",
                "id": 1,
            },
        },
    )
    requests_mock.get(
        "https://example.com/11.jpeg",
        content=b"TEST",
        headers={"Content-Type": "image/jpeg"},
    )

    image = get_new_image()
    assert image
    assert image.image_file


@pytest.mark.django_db
def test_get_image_doesnt_exist(requests_mock):
    """
    Check exception is raised for missing image / non success response
    """
    Image.objects.create(external_id=10)
    requests_mock.get(
        "https://api.slingacademy.com/v1/sample-data/photos/11",
        json={
            "success": False,
        },
    )

    with pytest.raises(GetImageException):
        get_new_image()


@pytest.mark.django_db
def test_get_image_exists_cant_fetch_url(requests_mock):
    """
    Check exception is raised when image cannot be fetched
    """
    Image.objects.create(external_id=10)
    requests_mock.get(
        "https://api.slingacademy.com/v1/sample-data/photos/11",
        json={
            "success": True,
            "photo": {
                "url": "https://example.com/11.jpeg",
                "id": 1,
            },
        },
    )
    requests_mock.get(
        "https://example.com/11.jpeg",
        status_code=404,
    )

    with pytest.raises(GetImageException):
        get_new_image()
