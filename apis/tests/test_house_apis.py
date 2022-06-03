import pytest
from django.shortcuts import reverse
from apis.tests.utils import create_myhome_data

pytestmark = pytest.mark.django_db


@pytest.mark.parametrize(
    "target, region",
    [("신혼부부", "서울특별시"), ("신혼부부", "경기도"), ("대학생", "서울특별시"), ("대학생", "경기도")],
)
def test_read_myhome_with_cs(client, target, region):
    url = reverse("myhome-list") + f"?target={target}&region={region}"

    create_myhome_data(target, region, 10)

    response = client.get(url)
    response_data = response.json()

    assert response_data["results"][0]["region"] == region
    assert response.status_code == 200
