from flask import Blueprint, request, jsonify
from util.staff_apply import *

apply = Blueprint('apply', __name__)

@apply.route("/api/apply", methods=['POST'])
def staff_apply():
    data = request.get_json()
    if not data:
        return jsonify({"error": "Invalid JSON or no data provided"}), 400
    
    required_fields = ["staff_id", "request_type", "start_date", "end_date", "recurrence_days", "is_am", "is_pm", "apply_date", "request_reason"]
    for field in required_fields:
        if field not in data:
            return jsonify({"error": f"Missing '{field}' in request"}), 400

    if data.get("request_type") == "Ad-hoc":
        return handle_adhoc_request(data)
    
    elif data.get("request_type") == "Recurring":
        return handle_recurring_request(data)
    
    else:
        return jsonify({"error": "Invalid request type"}), 400
    