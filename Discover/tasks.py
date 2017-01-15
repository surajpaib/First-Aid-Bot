from celery.schedules import crontab
from celery.decorators import periodic_task
from celery.utils.log import get_task_logger



logger = get_task_logger(__name__)

@periodic_task(run_every=(crontab(minute='*/1')), name="some_task", ignore_result=True)
def some_task():
    logger.info("Hello")
    print "Helo"