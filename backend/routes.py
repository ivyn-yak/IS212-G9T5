from flask import Blueprint, jsonify
import json
from models import *

# Define a blueprint
main = Blueprint('main', __name__)

@main.route("/")
def config():
    return {"hello":"world"}

##### EMPLOYEE TABLE #####
@main.route("/all")
def get_org_data():
    data = Employee.query.all()
    return jsonify([employee.json() for employee in data])

@main.route("/staff/<int:staff_id>")
def get_staff_data(staff_id):
    employee = Employee.query.filter_by(staff_id=staff_id).first()

    if employee is None:
        return jsonify({'error': 'Employee not found'}), 404

    return jsonify(employee.json())

@main.route("/team/<int:staff_id>")
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