from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import os

app = Flask(__name__)

# Configure PostgreSQL database URI
POSTGRES_USER = os.getenv("POSTGRES_USER")
POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD")
POSTGRES_HOST = os.getenv("POSTGRES_HOST")
POSTGRES_DB = os.getenv("POSTGRES_DB")

# PostgreSQL URI format: postgresql://username:password@host:port/database_name
app.config['SQLALCHEMY_DATABASE_URI'] = f"postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}/{POSTGRES_DB}"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
CORS(app, supports_credentials=True)

@app.route("/")
def config():
    print(POSTGRES_USER)
    return {"hello":"world"}


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001, debug=True)