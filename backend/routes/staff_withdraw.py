from flask import Blueprint, request, jsonify
from datetime import date
from models import *
from util.wfh_requests import *
from util.wfh_request_logs import *

withdraw = Blueprint('withdraw', __name__)

@withdraw.route("/api/withdraw", methods=['POST'])
def staff_withdraw():
    data = request.get_json()
    if not data:
        return jsonify({"error": "Invalid JSON or no data provided"}), 400
    
    required_fields = ["request_id", "reason", "specific_date"]
    for field in required_fields:
        if field not in data:
            return jsonify({"error": f"Missing '{field}' in request"}), 400
    
    request_id = data["request_id"]
    specific_date = data["specific_date"]
    reason = data["reason"]

    try:
        req = get_request(request_id, specific_date)
        if not req:
            return jsonify({"error": "Request not found"}), 400

        if req["request_status"] != "Approved":
            return jsonify({"error": "Request has not been approved."}), 400
        
        updated_fields = {
            "request_status": "Pending_Withdraw",
            "apply_date": date.today().strftime('%Y-%m-%d'),
            "request_reason": reason
        }

        new_req = update_request(request_id, specific_date, updated_fields)
        if new_req is None:
            return jsonify({"error": "Request not found"}), 404
        
        log_wfh_request(new_req["new_request"])

        return jsonify({
            "message": "Withdraw request successfully created.",
            "request": new_req["new_request"]
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500