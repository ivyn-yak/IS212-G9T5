from flask import Blueprint, jsonify
from models import *
from util.employee import *

employee = Blueprint('employee', __name__)

##### EMPLOYEE TABLE #####
@employee.route("/api/all")
def get_org_data():
    data = Employee.query.all()
    return jsonify([employee.json() for employee in data])

@employee.route("/api/staff/<int:staff_id>")
def get_staff_data(staff_id):
    employee = get_employee_by_id(staff_id)
    if "error" in employee:
        return jsonify({"staff_id": staff_id}), 404
    return jsonify(employee)

@employee.route("/api/team/<int:staff_id>")
def get_team_data(staff_id):
    employee, error_response, error_code = get_employee_by_id(staff_id)
    
    if error_response:
        return error_response, error_code

    if employee.role == 2:  # If the employee is a role 2 (non-manager), get their manager's team
        rm_id = employee.reporting_manager    
    else:
        rm_id = staff_id
    
    team = get_full_team(rm_id)

    return jsonify([employee.json() for employee in team])
