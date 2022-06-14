from celery import shared_task
from celery.utils.log import get_task_logger
from schedules.celery_beat import MyHomeUpdater


logger = get_task_logger(__name__)


@shared_task
def sample_task():
    logger.info("The sample task just ran.")


@shared_task
def myhome_update():
    myhome_cs = MyHomeUpdater("couple", "seoul")
    myhome_ck = MyHomeUpdater("couple", "kkd")
    myhome_ss = MyHomeUpdater("student", "seoul")
    myhome_sk = MyHomeUpdater("student", "kkd")

    logger.info("myhome update is ready")

    myhome_cs.update()
    myhome_ck.update()
    myhome_ss.update()
    myhome_sk.update()
