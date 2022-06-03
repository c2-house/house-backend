import re
import logging
import pandas as pd
from django.core.management.base import BaseCommand, CommandError
from apis.models import MyHome, StationArea

logger = logging.getLogger(__name__)


class Command(BaseCommand):

    help = "CSV 데이터 bulk_create"

    def add_arguments(self, parser):
        parser.add_argument("--path", type=str, help="csv파일 경로 입력")
        parser.add_argument(
            "--target",
            default="신혼부부",
            choices=["신혼부부", "대학생"],
            type=str,
            help="신혼부부 or 대학생",
        )

    def handle(self, *args, **kwargs):
        path = kwargs.get("path")
        target = kwargs.get("target")

        try:
            file_type = self._check_csv_file(path)
            data = self._read_csv(path)
        except ValueError as e:
            logger.error(e)
            raise CommandError(e)
        else:
            self._create(data, file_type, target)
        finally:
            logger.info(f"{len(data)}개의 데이터 저장 완료")

    def _check_csv_file(self, path):
        file_check = re.findall("myhome|my_home|sa|sh", path)
        if not file_check:
            raise ValueError("파일 이름에 myhome, my_home, sa, sh가 포함되어 구분 해야함")
        return file_check

    def _read_csv(self, path):
        data = pd.read_csv(path)
        return data

    def _create(self, data, file_type, target):
        house_instances = []

        def status_to_bool(status):
            if status == "모집중":
                return True
            else:
                return False

        if ("myhome" in file_type) or ("my_home" in file_type):
            for i in data.itertuples():
                house_instances.append(
                    MyHome(
                        supply_type=i[1],
                        status=status_to_bool(i[2]),
                        region=i[3],
                        title=i[4],
                        registration_date=i[5],
                        release_date=i[6],
                        supplier=i[7],
                        link=i[8],
                        target=target,
                    )
                )
            MyHome.objects.bulk_create(house_instances)

        elif "sa" in file_type:
            for i in data.itertuples():
                house_instances.append(
                    StationArea(
                        index=i[1],
                        supply_type=i[2],
                        title=i[3],
                        registration_date=i[4],
                        apply_date=i[5],
                        supplier=i[6],
                        link=i[7],
                    )
                )
            StationArea.objects.bulk_create(house_instances)
