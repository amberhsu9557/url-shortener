import logging
import time
import requests
import redis
# from pymongo import MongoClient
from celery_chef import app
from celery.task.schedules import crontab
from celery.decorators import periodic_task
from celery.utils.log import get_task_logger

LOGGER = get_task_logger(__name__)

# client = MongoClient('10.1.1.234', 27018) # change the ip and port to your mongo database's
# db = client.mongodb_test
# collection = db.celery_test
# post = db.test

# @app.on_after_configure.connect
# def setup_periodic_tasks(sender, **kwargs):
#     # Calls test('hello') every 10 seconds.
#     sender.add_periodic_task(10.0, get_word.s('hello'), name='add every 10')

#     # Calls test('world') every 30 seconds
#     sender.add_periodic_task(30.0, get_word.s('world'), expires=10)

#     # Executes every Monday morning at 7:30 a.m.
#     sender.add_periodic_task(
#         crontab(hour=7, minute=30, day_of_week=1),
#         get_word.s('Happy Mondays!'),
#     )

# app.conf.beat_schedule = {
#     'add-every-5-seconds': {
#         'task': 'tasks.add',
#         'schedule': 5.0,
#         # # # Executes every Monday morning at 7:30 a.m.
#         # 'schedule': crontab(hour=7, minute=30, day_of_week=1),
#         'args': (16, 16)
#     },
# }

@periodic_task(run_every=5,
                queue='crawler',
                options={'queue': 'crawler'})
def add():
    return 'update all GPU docker status to cache file'

@app.task(bind=True,default_retry_delay=10) # set a retry delay, 10 equal to 10s
def longtime_add(self,i):
    print ('long time task begins')
    try:
        r = requests.get(i)
        # post.insert({'status':r.status_code,"creat_time":time.time()}) # store status code and current time to mongodb
        print ('long time task finished')
    except Exception as exc:
        raise self.retry(exc=exc)
    return r.status_code