import pytest
from django.shortcuts import reverse
from apis.tests.utils import create_myhome_data

pytestmark = pytest.mark.django_db


def test_read_myhome_with_cs(client):
    target = "신혼부부"
    region = "서울특별시"
    url = reverse("myhome-list") + f"?target={target}&region={region}"

    create_myhome_data(target, region, 10)

    response = client.get(url)
    response_data = response.json()

    assert response_data["results"][0]["region"] == "서울특별시"
    assert response.status_code == 200
