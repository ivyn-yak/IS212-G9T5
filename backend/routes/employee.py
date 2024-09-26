from flask import Blueprint, jsonify
from models import *

employee = Blueprint('employee', __name__)

##### EMPLOYEE TABLE #####
@employee.route("/api/all")
def get_org_data():
    data = Employee.query.all()
    return jsonify([employee.json() for employee in data])

@employee.route("/api/staff/<int:staff_id>")
def get_staff_data(staff_id):
    employee = Employee.query.filter_by(staff_id=staff_id).first()

    if employee is None:
        return jsonify({'error': 'Employee not found'}), 404

    return jsonify(employee.json())

@employee.route("/api/team/<int:staff_id>")
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
