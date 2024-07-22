import pytest
from model_bakery import baker


@pytest.mark.django_db
def test_chat_is_created_for_user():
    user = baker.make("users.User")
    assert user.chat
