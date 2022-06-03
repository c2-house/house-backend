from mixer.backend.django import mixer
from apis.models import MyHome


def create_myhome_data(target, region, count):
    mixer.cycle(count).blend(MyHome, target=target, region=region)
