from flask import Flask

from celery_config import init_celery

# create Flask app
app = Flask(__name__)

# config celery and initialize
app.config["CELERY_BROKER_URL"] = "pyamqp://guest:guest@localhost//"

# Initialize Celery
celery = init_celery(app)
celery.conf.update(app.config)


if __name__ == "__main__":
    # run app
    app.run(debug=True)
