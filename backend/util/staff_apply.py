from flask import jsonify
from datetime import date, datetime
from models import *
from util.employee import *
from util.wfh_requests import *
import uuid

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
        
        specific_date = data['specific_date']
        request = check_staff_request(staff_id, specific_date)
        if request:
            return jsonify({"error": f"Staff has an existing request for {specific_date}"}), 400

        new_uuid = uuid.uuid4()
        uuid_string = str(new_uuid)

        new_request = WFHRequests(
            request_id=uuid_string,
            staff_id=staff_id,
            manager_id=rm_id,
            specific_date=date.fromisoformat(data['specific_date']),
            is_am=data['is_am'],
            is_pm=data['is_pm'], 
            request_status= "Pending",  
            apply_date=date.fromisoformat(data['apply_date']),
            request_reason=data.get('request_reason')
        )

        db.session.add(new_request)

        new_request_log = WFHRequestLogs(
            log_datetime=datetime.now(),  
            request_id=new_request.request_id,
            specific_date=new_request.specific_date,
            request_status=new_request.request_status,  
            apply_log_date=new_request.apply_date,
            reason_log=new_request.request_reason
        )

        db.session.add(new_request_log)
        db.session.commit()

        return jsonify({
            "message": "Ad-hoc request successfully created.",
            "request": new_request.json()
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500
    

def handle_recurring_request(data):
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

        recurrence_days = data.get('recurrence_days')
        if recurrence_days is None:
            return jsonify({"error": "Recurrence days not provided"}), 400

        new_request = WFHRequests(
            staff_id=staff_id,
            manager_id=rm_id,
            request_type=data['request_type'],  
            start_date=date.fromisoformat(data['start_date']),  
            end_date=date.fromisoformat(data['end_date']),
            recurrence_days=data.get('recurrence_days', None),
            is_am=data['is_am'],
            is_pm=data['is_pm'], 
            request_status= "Pending",  
            apply_date=date.fromisoformat(data['apply_date']),
            withdraw_reason=None,
            request_reason=data.get('request_reason')
        )
        
        db.session.add(new_request)
        db.session.commit()

        return jsonify({
            "message": "Recurring request successfully created.",
            "request": new_request.json()
        }), 201
        
    except Exception as e:
        print(f"Error occurred: {e}")
        db.session.rollback()
        return jsonify({"error": str(e)}), 500
    
