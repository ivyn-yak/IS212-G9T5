from flask import Blueprint, request, jsonify
from util.staff_apply import *

requests = Blueprint('requests', __name__)

@requests.route("/api/<int:staff_id>")
def get_requests(staff_id):
    employee = get_employee_by_id(staff_id)
    if not employee:
        return jsonify({"error": "Staff not found"}), 404
    
    employee_requests = WFHRequests.query.filter(WFHRequests.staff_id == staff_id).all()
    if not employee_requests:
        return jsonify({"data": []}), 200

    data = [request.json() for request in employee_requests]

    return jsonify({"data":data}), 200

@requests.route("/api/<int:staff_id>/pending")
def get_pending(staff_id):
    employee = get_employee_by_id(staff_id)
    if not employee:
        return jsonify({"error": "Staff not found"}), 404
    
    employee_requests = WFHRequests.query.filter(
        (WFHRequests.staff_id == staff_id) & 
        (WFHRequests.request_status == 'Pending')
    ).all()
    if not employee_requests:
        return jsonify({"data": []}), 200

    data = [request.json() for request in employee_requests]

    return jsonify({"data":data}), 200


