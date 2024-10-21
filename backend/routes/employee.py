from flask import Blueprint, jsonify
from models import *
from util.employee import *

employee = Blueprint('employee', __name__)

##### EMPLOYEE TABLE #####
@employee.route("/api/all")
def get_org_data():
    data = Employee.query.all()
    return jsonify([employee.json() for employee in data])

@employee.route("/api/<int:staff_id>")
def get_staff_data(staff_id):
    employee = get_employee_by_id(staff_id)
    if not employee:
        return jsonify({"error": f"Staff {staff_id} not found"}), 404
    return jsonify(employee)

@employee.route("/api/role/<int:staff_id>")
def get_staff_role(staff_id):
    employee = get_employee_by_id(staff_id)
    if not employee:
        return jsonify({"error": f"Staff {staff_id} not found"}), 404
    
    role = employee["role"]
    return jsonify({"staff_id": staff_id, "role": role })

@employee.route("/api/team/<int:staff_id>")
def get_team_data(staff_id):
    employee= get_employee_by_id(staff_id)
    if not employee:
        return jsonify({"error": f"Staff {staff_id} not found"}), 404

    if employee["role"] == 2:  # If the employee is a role 2 (non-manager), get their manager's team
        rm_id = employee["reporting_manager"]    
    else:
        rm_id = staff_id
    
    team = get_full_team(rm_id)

    return jsonify([employee.json() for employee in team])
