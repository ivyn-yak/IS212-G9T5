from flask import Flask
from flask_cors import CORS
import os
from dotenv import load_dotenv
from models import db
from routes.config import config
from routes.employee import employee
from routes.wfh_dates import dates
from routes.staff_apply import apply
from routes.manager_approve import approve
from routes.staff_requests import requests
from routes.staff_withdraw import withdraw

from app.utils import celery_init_app
from app import task
from celery.schedules import crontab

load_dotenv()

def create_app():
    app = Flask(__name__)

    DATABASE_URL = os.getenv("DATABASE_URL")
    app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_URL
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config.from_mapping(
        CELERY=dict(
            broker_url="redis://localhost:6379",
            result_backend="redis://localhost:6379",
            task_ignore_result=True,
            beat_schedule={
                # FOR TESTING
                # "task-every-night-midnight": {
                #     "task": "app.task.hello_world",
                #     "schedule": 10,
                # },
                "task-auto-rej-every-night-midnight": {
                    "task": "app.task.auto_reject",
                    "schedule": crontab(hour=0, minute=0),
                }
            },
        ),
    )

    CORS(app, supports_credentials=True)

    app.register_blueprint(config)
    app.register_blueprint(employee)
    app.register_blueprint(dates)
    app.register_blueprint(apply)
    app.register_blueprint(approve)
    app.register_blueprint(requests)
    app.register_blueprint(withdraw)

    db.init_app(app)

    celery_init_app(app)

    return app

app = create_app()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001, debug=True)