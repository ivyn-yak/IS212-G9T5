from flask import Blueprint, jsonify, request
from models import *
from util.wfh_requests import *
from util.request_decisions import *
from util.wfh_dates import *
from datetime import timedelta
from datetime import date
from sqlalchemy import and_

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
        
        staff_id = req["staff_id"]
        employee = Employee.query.filter_by(staff_id=staff_id).first()
        # if not employee: 
        #     return jsonify({"error": f"Employee with staff_id {staff_id} not found"}), 404
        
        reporting_manager_id = employee.reporting_manager
        if not reporting_manager_id:
            return jsonify({"error": f"Reporting manager for employee {staff_id} not found"}), 404
        
        employees_under_same_manager = Employee.query.filter_by(reporting_manager=reporting_manager_id).all()
        total_employees = len(employees_under_same_manager)
        
        start_date = req["start_date"]
        is_am = req["is_am"]
        is_pm = req["is_pm"]

        if is_am:
            approved_am_requests = WFHRequestDates.query.filter(
                and_(
                    WFHRequestDates.staff_id.in_([emp.staff_id for emp in employees_under_same_manager]),
                    WFHRequestDates.specific_date == start_date,
                    WFHRequestDates.decision_status.in_(['Approved', 'Pending Withdraw']),
                    WFHRequestDates.is_am == True  # Check for AM session
                )
            ).count()

            if total_employees > 0:
                ratio_am = (approved_am_requests + 1) / total_employees
            else:
                ratio_am = 0

            if ratio_am > 0.5:
                return jsonify({"error": "Exceed 0.5 rule limit for AM session"}), 422

        if is_pm:
            approved_pm_requests = WFHRequestDates.query.filter(
                and_(
                    WFHRequestDates.staff_id.in_([emp.staff_id for emp in employees_under_same_manager]),
                    WFHRequestDates.specific_date == start_date,
                    WFHRequestDates.decision_status.in_(['Approved', 'Pending Withdraw']),
                    WFHRequestDates.is_pm == True  # Check for PM session
                )
            ).count()

            if total_employees > 0:
                ratio_pm = (approved_pm_requests + 1) / total_employees
            else:
                ratio_pm = 0

            if ratio_pm > 0.5:
                return jsonify({"error": "Exceed 0.5 rule limit for PM session"}), 422

        # approved_requests = WFHRequestDates.query.filter(
        #     and_(
        #         WFHRequestDates.staff_id.in_([emp.staff_id for emp in employees_under_same_manager]),
        #         WFHRequestDates.specific_date == start_date,
        #         WFHRequestDates.decision_status.in_(['Approved', 'Pending Withdraw']),
        #         WFHRequestDates.is_am == is_am, 
        #         WFHRequestDates.is_pm == is_pm, 
        #     )
        # ).count()

        # if total_employees > 0:
        #     ratio = (approved_requests+1) / total_employees
        # else:
        #     ratio = 0

        # if ratio > 0.5:
        #     return jsonify({"error": "Exceed 0.5 rule limit"}), 422
        

        # print(f"Calling update_request with request_id: {request_id}")
        new_req = update_request(request_id, {"request_status": data.get("decision_status")})
        # print(f"update_request returned: {new_req}")
        if new_req is None:
            return jsonify({"error": "Request not found"}), 404

        # print(f"Calling create_request_decision with data: {data}")
        decision = create_request_decision(data)
        # print(f"create_request_decision returned: {decision}")
        if "error" in decision:
            return jsonify(decision), 500
        
        wfh_date = add_approved_date(new_req['new_request'], decision["decision"]["decision_status"])
        if "error" in wfh_date:
            return jsonify(wfh_date), 500 
        
        return jsonify({
            "message": "Request updated and manager's decision stored successfully",
            "request": new_req["new_request"],
            "decision": decision["decision"],
            "wfh_date": wfh_date["wfh_date"]
        }), 201

    except Exception as e:
        db.session.rollback() 
        print(f"Error: {str(e)}")
        return jsonify({"error": str(e)}), 500

@approve.route("/api/approve_recurring", methods=['POST'])

def manager_approve_recurring():
    data = request.get_json()
    if not data:
        return jsonify({"error": "Invalid JSON or no data provided"}), 400

    try:
        request_id = data["request_id"]
        req = get_request(request_id)
        if not req:
            return jsonify({"error": "Request not found"}), 404

        staff_id = req["staff_id"]
        employee = Employee.query.filter_by(staff_id=staff_id).first()
        # if not employee:
        #     return jsonify({"error": f"Employee with staff_id {staff_id} not found"}), 404

        reporting_manager_id = employee.reporting_manager
        if not reporting_manager_id:
            return jsonify({"error": f"Reporting manager for employee {staff_id} not found"}), 404

        employees_under_same_manager = Employee.query.filter_by(reporting_manager=reporting_manager_id).all()
        total_employees = len(employees_under_same_manager)

        start_date = date.fromisoformat(req["start_date"])
        end_date = date.fromisoformat(req["end_date"])
        recurrence_days = req["recurrence_days"]
        is_am = req["is_am"]
        is_pm = req["is_pm"]


        if not recurrence_days:
            return jsonify({"error": "Recurrence days not specified"}), 400

        day_mapping = {
            'monday': 0,
            'tuesday': 1,
            'wednesday': 2,
            'thursday': 3,
            'friday': 4,
            'saturday': 5,
            'sunday': 6
        }

        try:
            recurrence_day_int = day_mapping[recurrence_days.strip().lower()] if recurrence_days.strip().lower() in day_mapping else int(recurrence_days)
        except (ValueError, KeyError):
            return jsonify({"error": "Invalid recurrence day format"}), 400

        recurring_dates = []
        current_date = start_date
        while current_date <= end_date:
            if current_date.weekday() == recurrence_day_int:
                recurring_dates.append(current_date)
            current_date += timedelta(days=1)

        for current_date in recurring_dates:
            # Check the 0.5 rule for each date
            approved_requests = WFHRequestDates.query.filter(
                and_(
                    WFHRequestDates.staff_id.in_([emp.staff_id for emp in employees_under_same_manager]),
                    WFHRequestDates.specific_date == start_date,
                    WFHRequestDates.decision_status.in_(['Approved', 'Pending Withdraw']),
                    WFHRequestDates.is_am == is_am, 
                    WFHRequestDates.is_pm == is_pm, 
                )
            ).count()


            if total_employees > 0:
                ratio = (approved_requests + 1) / total_employees
            else:
                ratio = 0

            if ratio > 0.5:
                return jsonify({
                    "error": f"Exceed 0.5 rule limit for date {current_date.isoformat()}",
                    "failed_date": current_date.isoformat()
                }), 422
            
        for current_date in recurring_dates:
            decision = create_request_decision(data)
            if "error" in decision:
                return jsonify({"error": f"Error creating decision for date {current_date}: {decision['error']}"}), 500

        # Update the original request status
        update_request(request_id, {"request_status": data.get("decision_status")})

        return jsonify({
            "message": "Recurring WFH requests processed successfully",
            "request": req,
            "recurring_dates": [date.isoformat() for date in recurring_dates],
        }), 201

    except Exception as e:
        db.session.rollback()
        print(f"Error: {str(e)}")
        return jsonify({"error": str(e)}), 500