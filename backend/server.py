from flask import Flask
from flask_cors import CORS
import os
from models import db
from routes import main

app = Flask(__name__)

# Configure PostgreSQL database URI
POSTGRES_USER = os.getenv("POSTGRES_USER")
POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD")
POSTGRES_HOST = os.getenv("POSTGRES_HOST")
POSTGRES_DB = os.getenv("POSTGRES_DB")

# PostgreSQL URI format: postgresql://username:password@host:port/database_name
app.config['SQLALCHEMY_DATABASE_URI'] = f"postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}/{POSTGRES_DB}"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)
CORS(app, supports_credentials=True)

app.register_blueprint(main)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001, debug=True)