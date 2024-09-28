from flask import Flask
from flask_cors import CORS
import os
from dotenv import load_dotenv
from models import db
from routes.config import config
from routes.employee import employee
from routes.wfh_dates import dates
from routes.staff_apply import apply

load_dotenv()

app = Flask(__name__)

if __name__ == '__main__':
    DATABASE_URL = os.getenv("DATABASE_URL")
    app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_URL
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite://"

db.init_app(app)

CORS(app, supports_credentials=True)

app.register_blueprint(config)
app.register_blueprint(employee)
app.register_blueprint(dates)
app.register_blueprint(apply)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001, debug=True)