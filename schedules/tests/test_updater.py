import pytest
import pandas as pd
from schedules.tasks import MyHomeUpdater
from mixer.backend.django import mixer
from apis.models import MyHome


pytestmark = pytest.mark.django_db


def mock_new_data(*args, **kwargs):
    dummy_data = {
        "공급유형": ["행복주택"] * 4,
        "진행상태": ["모집중"] * 4,
        "지역": ["경기도"] * 4,
        "공고명": [
            "안산 선부 행복주택 예비입주자 모집공고",
            "경기도,평택시·안성시 지역 행복주택 예비입주자 모집",
            "경기도,남양뉴타운 B9 · B10블록 행복주택 입주자격완화 추가모집 공고",
            "old 데이터 중복",
        ],
        "모집공고일자": ["2022-05-31", "2022-05-30", "2022-05-27", "2022-05-27"],
        "당첨발표일자": ["2022-09-23", "2022-10-13", "2022-09-21", "2022-09-21"],
        "공급기관": ["안산도시공사", "LH", "LH", "old"],
        "링크": [
            "https://www.myhome.go.kr/hws/portal/sch/selectRsdtRcritNtcDetailView.do?pblancId=8601",
            "https://www.myhome.go.kr/hws/portal/sch/selectRsdtRcritNtcDetailView.do?pblancId=11490",
            "https://www.myhome.go.kr/hws/portal/sch/selectRsdtRcritNtcDetailView.do?pblancId=11483",
            "https://www.google.com",
        ],
    }

    data_frame = pd.DataFrame(dummy_data)

    return data_frame


def mock_old_data(*args, **kwargs):
    mixer.cycle(10).blend(MyHome, link="https://www.google.com")
    data = MyHome.objects.all()
    return data


def test_myhome_update(mocker):
    mocker.patch("schedules.tasks.MyhomeDataHandler.get_new_data", mock_new_data)
    mocker.patch("schedules.tasks.MyhomeDataHandler.get_old_data", mock_old_data)

    updater = MyHomeUpdater("student", "kkd")
    updater.update()

    assert (
        MyHome.objects.last().link
        == "https://www.myhome.go.kr/hws/portal/sch/selectRsdtRcritNtcDetailView.do?pblancId=11483"
    )
