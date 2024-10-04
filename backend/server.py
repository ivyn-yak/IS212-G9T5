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
from werkzeug.middleware.dispatcher import DispatcherMiddleware

load_dotenv()

app = Flask(__name__)

DATABASE_URL = os.getenv("DATABASE_URL") if os.getenv("DATABASE_URL") else "sqlite://"
app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_URL
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

CORS(app, supports_credentials=True)

app.register_blueprint(config)
app.register_blueprint(employee)
app.register_blueprint(dates)
app.register_blueprint(apply)
app.register_blueprint(approve)

# Apply DispatcherMiddleware
application = DispatcherMiddleware(app, {
    '/api': app
})

if __name__ == "__main__":
    from werkzeug.serving import run_simple
    run_simple('0.0.0.0', 5001, application, use_reloader=True, use_debugger=True)
