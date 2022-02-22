import os
import logging
from apscheduler.jobstores.sqlalchemy import SQLAlchemyJobStore
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from django.conf import settings
# from pytz import timezone

from apps.api_test.task_mgr.scheduler import Scheduler


api_test_dir = os.path.abspath(os.path.join(os.path.dirname(__file__)))
logger = logging.getLogger("api_test")


def init_scheduler():
    # SQLAlchemyJobStore指定存储链接
    sqlalchemy_database_uri = ''
    db = settings.DATABASES.get('default')
    if db.get('ENGINE') == 'django.db.backends.sqlite3':
        db_path = os.path.abspath(os.path.join(api_test_dir, '../../db.sqlite3'))
        sqlalchemy_database_uri = 'sqlite:///{}'.format(db_path)
    elif db.get('ENGINE') == 'django.db.backends.mysql':
        user = db.get('USER')
        password = db.get('PASSWORD')
        host = db.get('HOST')
        port = db.get('PORT')
        name = db.get('NAME')
        sqlalchemy_database_uri = 'mysql+mysqlconnector://{}:{}@{}:{}/{}'.format(user, password, host, port, name)
    else:
        logger.critical("错误的数据库类型")

    if sqlalchemy_database_uri:
        job_store = {
            'default': SQLAlchemyJobStore(
                url=sqlalchemy_database_uri,
                tablename='testtask',
                engine_options={
                    "logging_name": "api_test",
                    "pool_recycle": 1500
                },
                pickle_protocol=3
            )
        }
        scheduler = AsyncIOScheduler()
        Scheduler.init(scheduler)
        Scheduler.configure(jobstores=job_store)  # , timezone=timezone('Asia/Shanghai')
        Scheduler.start()


try:
    init_scheduler()
except Exception as e:
    logger.warning(e)
