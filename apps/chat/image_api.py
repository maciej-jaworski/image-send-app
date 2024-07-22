import sys
from io import BytesIO

import requests
from chat.models import Image
from django.core.files.uploadedfile import InMemoryUploadedFile

API_URL = "https://api.slingacademy.com/v1/sample-data/photos/{}"


class GetImageException(Exception):

    def __init__(self, message, *args, **kwargs):
        self.message = message
        super().__init__(*args, **kwargs)


def get_new_image():
    try:
        latest_image = Image.objects.exclude(external_id=None).latest("external_id")
        image_id_to_fetch = latest_image.external_id + 1
    except Image.DoesNotExist:
        image_id_to_fetch = 1

    image_metadata_response = requests.get(API_URL.format(image_id_to_fetch))

    if not image_metadata_response.ok:
        raise GetImageException(
            f"Could not fetch image from remote API, bad response {image_metadata_response.status_code}"
        )

    image_metadata = image_metadata_response.json()

    if not image_metadata["success"]:
        raise GetImageException("Remote API didn't return any images.")

    image_url = image_metadata["photo"]["url"]
    image_data_response = requests.get(image_url)

    if not image_data_response.ok:
        raise GetImageException(
            f"Image could not be downloaded {image_data_response.status_code}"
        )

    image_file_contents = BytesIO(image_data_response.content)

    return Image.objects.create(
        external_id=image_metadata["photo"]["id"],
        image_file=InMemoryUploadedFile(
            file=image_file_contents,
            field_name=None,
            name=image_url.split("/")[-1],
            content_type=image_data_response.headers["Content-Type"],
            size=image_file_contents.tell(),
            charset=sys.getfilesystemencoding(),
        ),
    )
