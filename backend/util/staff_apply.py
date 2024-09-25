from flask import jsonify
from datetime import date, timedelta
from ..models import *

def handle_adhoc_request(data):
    try:
        # TO DO: implement head count check for that day 

        add_req = apply_wfh(data)  # Add to WFH requests table

        if "error" in add_req:
            return jsonify(add_req), 400
        
        # Successfully added the request, now handle the WFH date entry
        request = add_req["request"]

        date_data = {
            "request_id": request.request_id,
            "specific_date": request.start_date,
            "staff_id": request.staff_id,
            "is_am": request.is_am,
            "is_pm": request.is_pm
        }

        add_date = add_wfh_date(date_data)  # Add to WFH dates table

        if "error" in add_date:
            return jsonify(add_date), 400
        
        return jsonify({
            "message": "Ad-hoc request and date successfully added.",
            "request": add_req
        }), 201

    except Exception as e:
        return jsonify({"error": str(e)}), 500

def apply_wfh(data):
    try:
        apply_date=date.fromisoformat(data['apply_date'])
        withdrawable_until = apply_date + timedelta(weeks=2)

        new_request = WFHRequests(
            staff_id=data['staff_id'],
            request_type=data['request_type'],  
            start_date=date.fromisoformat(data['start_date']),  
            end_date=date.fromisoformat(data['end_date']),
            recurrence_days=data.get('recurrence_days'),
            is_am=data['is_am'],
            is_pm=data['is_pm'], 
            request_status= "Pending",  
            apply_date=apply_date,
            withdrawable_until=withdrawable_until,
            request_reason=data.get('request_reason')
        )
        
        db.session.add(new_request)
        db.session.commit()

        return {"message": "WFH request successfully applied!", "request": new_request}

    except Exception as e:
        db.session.rollback()
        return {"error": str(e)}
    
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


    

