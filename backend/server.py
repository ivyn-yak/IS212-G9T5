from flask import Flask
from flask_cors import CORS
import os
from dotenv import load_dotenv
from models import db
from routes import main

load_dotenv()

app = Flask(__name__)

DATABASE_URL = os.getenv("DATABASE_URL")
app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_URL
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

# Create the tables if they don't exist
with app.app_context():
    db.create_all()
CORS(app, supports_credentials=True)

app.register_blueprint(main)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001, debug=True)