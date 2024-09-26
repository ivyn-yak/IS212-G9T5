from flask import Blueprint, jsonify
from models import *

config = Blueprint('config', __name__)

@config.route("/api/")
def main():
    return {"hello":"world"}

##THIS CHECKS THE NAMES OF THE TABLES IN THE DB
@config.route("/api/check-tables", methods=['GET'])
def check_tables():
    # Use the inspector to get a list of tables
    inspector = inspect(db.engine)
    tables = inspector.get_table_names()
    return jsonify({"tables": tables})