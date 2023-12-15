import pymongo
from decouple import config
from flask import Flask, render_template
from flask_pymongo import PyMongo

import utils
from celery_config import init_celery
from utils.db_actions import get_all_properties

# from utils import db_actions

# create Flask app
app = Flask(__name__)

# config mondodb
app.config["MONGO_URI"] = config("MONGO_URL", "CHANGE ME")
mongo = PyMongo(app)

# config celery and initialize
app.config["CELERY_BROKER_URL"] = "pyamqp://guest:guest@localhost//"

# Initialize Celery
celery = init_celery(app)
celery.conf.update(app.config)


@app.route("/")
def index():
    return render_template("index.html", data=get_all_properties())


if __name__ == "__main__":
    # run app
    app.run(debug=True)

    # close browser on keyboard interrupt
    if KeyboardInterrupt:
        print("Exiting...")
        utils.browser.quit()
        exit()
