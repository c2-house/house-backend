from django.conf import settings
from house_info.my_home import MyHomeDataManager
from apis.models import MyHome


class MyhomeDataHandler:
    def __init__(self, target, region):
        self.chromedriver = settings.CHROME_DRIVER_PATH
        self.target = target
        self.region = region
        self.manager = self._get_manager()

    def _get_manager(self):
        manager = MyHomeDataManager(
            self.chromedriver, page=1, types=self.target, region=self.region
        )
        return manager

    def get_new_data(self):
        page_source = self.manager.create_page_sources()
        data_frame = self.manager.get_data_frame(page_source)
        return data_frame

    def get_old_data(self):
        data = MyHome.objects.filter(target=self.target, region=self.region)
        return data


class MyHomeUpdater:
    def __init__(self, target, region):
        self.target = target
        self.region = region

        try:
            self.data_handler = MyhomeDataHandler(self.target, self.region)
        except ValueError:
            pass
        else:
            self.old_data = self.data_handler.get_old_data()
            self.new_data = self.data_handler.get_new_data()

    def _exist_new_data(self):
        old_data = self.old_data.first()
        link = old_data.link

        if link == self.new_data["링크"][0]:
            return False
        return True

    def update(self):
        def status_to_bool(status):
            if status == "모집중":
                return True
            else:
                return False

        is_new_data = self._exist_new_data()
        data_for_update = []
        link_for_compare = self.old_data.first().link

        if is_new_data:
            for data in self.new_data.itertuples():
                if data[8] == link_for_compare:
                    break

                data_for_update.append(
                    MyHome(
                        supply_type=data[1],
                        status=status_to_bool(data[2]),
                        region=data[3],
                        title=data[4],
                        registration_date=data[5],
                        release_date=data[6],
                        supplier=data[7],
                        link=data[8],
                        target=self.target,
                    )
                )
            MyHome.objects.bulk_create(data_for_update)
