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

        day_mapping = {
            'monday': 0,
            'tuesday': 1,
            'wednesday': 2,
            'thursday': 3,
            'friday': 4,
            'saturday': 5,
            'sunday': 6
        }

# converting recurrence day to an integer to find the dates 
        try:
            recurrence_day_int = day_mapping[recurrence_days.strip().lower()] if recurrence_days.strip().lower() in day_mapping else int(recurrence_days)
        except (ValueError, KeyError):
            return jsonify({"error": "Invalid recurrence day format"}), 400

        recurring_dates = []
        start_date = data.get('start_date')
        end_date = data.get('end_date')
        current_date = start_date
        while current_date <= end_date:
            if current_date.weekday() == recurrence_day_int:
                recurring_dates.append(current_date)
            current_date += timedelta(days=1)

        # new_request = WFHRequests(
        #     staff_id=staff_id,
        #     manager_id=rm_id,
        #     request_type=data['request_type'],  
        #     start_date=date.fromisoformat(data['start_date']),  
        #     end_date=date.fromisoformat(data['end_date']),
        #     recurrence_days=data.get('recurrence_days', None),
        #     is_am=data['is_am'],
        #     is_pm=data['is_pm'], 
        #     request_status= "Pending",  
        #     apply_date=date.fromisoformat(data['apply_date']),
        #     withdraw_reason=None,
        #     request_reason=data.get('request_reason')
        # )
            
        for date in recurring_dates:
            new_request = WFHRequests(
                staff_id=staff_id,
                manager_id=rm_id,
                specific_date = date, 
                is_am = data.get('is_am'), 
                is_pm = data.get('is_pm'),
                request_status= "Pending",
                apply_date = date.fromisoformat(data['apply_date']),
                request_reason = data.get('request_reason')
            )
            db.session.add(new_request)
        
        # db.session.add(new_request)
        db.session.commit()

        return jsonify({
            "message": "Recurring requests successfully created.",
            "request": new_request.json()
        }), 201
        
    except Exception as e:
        print(f"Error occurred: {e}")
        db.session.rollback()
        return jsonify({"error": str(e)}), 500
    
