from flask import Blueprint, jsonify, request
from models import *
from util.wfh_requests import *
from util.request_decisions import *
from util.wfh_dates import *

approve = Blueprint('approve', __name__)

@approve.route("/api/approve", methods=['POST'])
def manager_approve_adhoc():
    data = request.get_json()
    if not data:
        return jsonify({"error": "Invalid JSON or no data provided"}), 400

    try: 
        request_id = data["request_id"]
        req = get_request(request_id)
        if not req:
            return jsonify({"error": "Request not found"}), 404

        # TO DO: head count check

        # update status in WFHRequests to decision
        new_req = update_request(request_id, {"request_status": data["decision"]})
        if new_req is None:
            return jsonify({"error": "Request not found"}), 404
        
        # store details in RequestDecisions
        decision = create_request_decision(data)
        if "error" in decision:
            return jsonify(decision), 500 
        
        # TO DO: populate WFHRequestDates 
        wfh_date = add_approved_date(new_req)
        if "error" in wfh_date:
            return jsonify(wfh_date), 500 
        
        return jsonify({"message": "Request updated and manager's decision stored successfully",
                        "request": new_req["request"],
                        "decision": decision.json(),
                        "wfh_date": wfh_date["wfh_date"]
                        }), 201

    except Exception as e:
        db.session.rollback() 
        return jsonify({"error": str(e)}), 500

    

