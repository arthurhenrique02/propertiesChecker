from celery import Celery
from celery.schedules import crontab
from flask import Flask


def init_celery(app: Flask) -> Celery:
    # create celery instance with the broker from app config
    celery = Celery(
        app.import_name,
        broker=app.config["CELERY_BROKER_URL"],
        # include scrapper task
        include=["utils.scrapper"],
    )

    celery.conf.update(app.config)

    # get daily properties list
    celery.conf.beat_schedule = {
        "get_properties_list_daily": {
            "task": "utils.scrapper.download_and_move_properties_list",
            "schedule": crontab(minute="1", hour="0", day_of_week="*"),
        },
    }

    # return instance
    return celery
