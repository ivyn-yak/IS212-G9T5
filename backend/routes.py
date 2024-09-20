from flask import Blueprint

# Define a blueprint
main = Blueprint('main', __name__)

@main.route("/")
def config():
    return {"hello":"world"}