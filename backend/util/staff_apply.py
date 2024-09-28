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
            recurrence_days=data.get('recurrence_days', ''),
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
    
def add_approved_date(request_id):
    pass 
    # TO DO: once request is approved, populate wfh dates table
    # Not implemented yet

    # request = get_request(request_id)
    # date_data = {
    #         "request_id": request.request_id,
    #         "specific_date": request.start_date,
    #         "staff_id": request.staff_id,
    #         "is_am": request.is_am,
    #         "is_pm": request.is_pm
    #     }

    # add_date = add_wfh_date(date_data)  # Add to WFH dates table

    # if "error" in add_date:
    #     return jsonify(add_date), 400
    
    # return jsonify({
    #     "message": "Ad-hoc dates successfully added.",
    #     "request": request
    # }), 201

def add_wfh_date(data):
    try: 
        new_date = WFHRequestDates(
            request_id=data["request_id"],
            specific_date=data["start_date"],
            staff_id=data["staff_id"],
            is_am=data["is_am"],
            is_pm=data["is_pm"]
            )
        
        db.session.add(new_date)
        db.session.commit()

        return {"message": "WFH date successfully added!", "wfh_date": new_date}

    except Exception as e:
        db.session.rollback()
        return {"error": str(e)}


    

