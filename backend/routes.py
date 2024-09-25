from flask import Blueprint, request, jsonify
import json
from models import *
from util.staff_apply import *

# Define a blueprint
main = Blueprint('main', __name__)

@main.route("/api/")
def config():
    return {"hello":"world"}

##### EMPLOYEE TABLE #####
@main.route("/api/all")
def get_org_data():
    data = Employee.query.all()
    return jsonify([employee.json() for employee in data])

@main.route("/api/staff/<int:staff_id>")
def get_staff_data(staff_id):
    employee = Employee.query.filter_by(staff_id=staff_id).first()

    if employee is None:
        return jsonify({'error': 'Employee not found'}), 404

    return jsonify(employee.json())

@main.route("/api/team/<int:staff_id>")
def get_team_data(staff_id):
    employee = Employee.query.filter_by(staff_id=staff_id).first()
    if employee is None:
        return jsonify({'error': 'Employee not found'}), 404

    role = employee.role

    if role == 2:
        rm_id = employee.reporting_manager
        team = Employee.query.filter_by(reporting_manager=rm_id).all()
    
    else:
        ids = []
        rm_id = staff_id
        team = Employee.query.filter_by(reporting_manager=rm_id).all()

        for employee in team:
            if employee.role != 2:
                ids.append(employee.staff_id)

        while ids:
            rm_id = ids.pop()
            subteam = Employee.query.filter_by(reporting_manager=rm_id).all()
            team += subteam

            for employee in subteam:
                if employee.role != 2:
                    ids.append(employee.staff_id)

    return jsonify([employee.json() for employee in team])

@main.route("/api/check-tables", methods=['GET'])
def check_tables():
    # Use the inspector to get a list of tables
    inspector = inspect(db.engine)
    tables = inspector.get_table_names()
    return jsonify({"tables": tables})

##### STAFF APPLY #####

@main.route("/api/apply", methods=['POST'])
def apply():

    data = request.get_json()
    if not data:
        return jsonify({"error": "Invalid JSON or no data provided"}), 400
    
    if data.get("request_type") == "Ad-hoc":
        return handle_adhoc_request(data)
    
    elif data.get("request_type") == "Recurring":
        pass
        # Not implemented yet
        # return handle_recurring_request(data)
    else:
        return jsonify({"error": "Invalid request type"}), 400
    
    


    