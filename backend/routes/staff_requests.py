from flask import Blueprint, request, jsonify
from datetime import datetime, timedelta
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

# Cancel a pending request
@requests.route("/api/staff/<int:staff_id>/cancel_request/<int:request_id>", methods=["PUT"])
def cancel_wfh_request(staff_id, request_id):
    # Fetch the request
    wfh_request = WFHRequests.query.filter_by(request_id=request_id, staff_id=staff_id).first()

    if not wfh_request:
        return jsonify({"error": "Request not found or not owned by this staff member"}), 404

    # Ensure the request is pending
    if wfh_request.request_status != 'pending':
        return jsonify({"error": "Only pending requests can be cancelled"}), 400

    # Check if the request falls within the allowed date range
    today = datetime.today().date()
    if wfh_request.start_date > today + timedelta(days=90) or wfh_request.start_date < today - timedelta(days=30):
        return jsonify({"error": "Requests can only be cancelled 3 months in advance and 1 month back"}), 400

    # Get the cancellation reason from the request body
    data = request.get_json()
    cancellation_reason = data.get("cancellation_reason")
    if not cancellation_reason:
        return jsonify({"error": "Cancellation reason is required"}), 400

    # Update request status and reason
    wfh_request.request_status = 'cancelled'
    wfh_request.request_reason = cancellation_reason
    db.session.commit()

    return jsonify({"message": "Request cancelled successfully"}), 200
