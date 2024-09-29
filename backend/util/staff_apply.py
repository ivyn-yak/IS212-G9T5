from flask import jsonify
from datetime import date, timedelta
from models import *
from util.employee import get_employee_by_id

def handle_adhoc_request(data):
    try:
        # get reporting manager
        staff_id = data["staff_id"]
        staff = get_employee_by_id(staff_id)
        if not staff:
            return jsonify({"error": "Staff not found"}), 404
        
        rm_id = staff["reporting_manager"]
        manager = get_employee_by_id(rm_id)
        if not manager:
            return jsonify({"error": "Manager not found"}), 404

        start_date=date.fromisoformat(data['start_date'])
        withdrawable_until = start_date + timedelta(weeks=2)

        new_request = WFHRequests(
            staff_id=staff_id,
            manager_id=rm_id,
            request_type=data['request_type'],  
            start_date=start_date,  
            end_date=date.fromisoformat(data['end_date']),
            recurrence_days=data.get('recurrence_days', None),
            is_am=data['is_am'],
            is_pm=data['is_pm'], 
            request_status= "Pending",  
            apply_date=date.fromisoformat(data['apply_date']),
            withdrawable_until=withdrawable_until,
            request_reason=data.get('request_reason')
        )
        
        db.session.add(new_request)
        db.session.commit()

        return jsonify({
            "message": "Ad-hoc request successfully created.",
            "request": new_request.json()
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500