import pytest
from django.shortcuts import reverse

pytestmark = pytest.mark.django_db


def test_read_myhome_with_cs(client):
    url = reverse("myhome_cs") + "?target=신혼부부&region=서울"
    response = client.get(url)
    assert response.status == 200
