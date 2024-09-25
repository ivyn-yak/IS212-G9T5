from flask import Blueprint, request, jsonify
from datetime import datetime, timedelta
import json
from models import *
from util.staff_apply import *
from util.employee import *

# Define a blueprint
main = Blueprint('main', __name__)

@main.route("/api/")
def config():
    return {"hello":"world"}

##### EMPLOYEE TABLE #####
@main.route("/api/all")
def get_org_data():
    employees = Employee.query.all()
    return jsonify([employee.json() for employee in employees])

@main.route("/api/staff/<int:staff_id>")
def get_staff_data(staff_id):
    employee, error_response, error_code = get_employee_by_id(staff_id)
    if error_response:
        return error_response, error_code

    return jsonify(employee.json())

@main.route("/api/team/<int:staff_id>")
def get_team_data(staff_id):
    employee, error_response, error_code = get_employee_by_id(staff_id)
    if error_response:
        return error_response, error_code

    # If the employee is a role 2 (non-manager), get their manager's team
    if employee.role == 2:
        rm_id = employee.reporting_manager
    else:
        rm_id = staff_id

    team = get_full_team(rm_id) # Get the full team (including all levels of reporting employees)
    
    return jsonify([employee.json() for employee in team])

##### WFHREQUESTDATES TABLE #####
# Get all wfh dates for a certain staff id
# GET /api/staff/1/wfh_dates
# [
#   {
#     "date_id": 1,
#     "request_id": 1,
#     "staff_id": 1,
#     "specific_date": "2024-09-24",
#     "is_am": true,
#     "is_pm": true
#   }
# ]
@main.route("/api/staff/<int:staff_id>/wfh_dates", methods=["GET"])
def get_staff_wfh_dates(staff_id):

    wfh_dates = WFHRequestDates.query.filter_by(staff_id=staff_id).all()

    if not wfh_dates:
        return jsonify({"message": "No WFH dates found for this staff member"}), 404

    return jsonify([date.json() for date in wfh_dates])

# Get all wfh dates for a certain staff id in a certain date range
#GET /api/staff/1/wfh_dates?start_date=2024-09-01&end_date=2024-09-30
# [
#   {
#     "date_id": 2,
#     "request_id": 2,
#     "staff_id": 1,
#     "specific_date": "2024-09-02",
#     "is_am": true,
#     "is_pm": false
#   }
# ]
@main.route("/api/staff/<int:staff_id>/wfh_dates", methods=["GET"])
def get_staff_wfh_dates_in_range(staff_id):
    start_date = request.args.get('start_date')
    end_date = request.args.get('end_date')

    if not start_date or not end_date:
        return jsonify({"error": "Please provide both start_date and end_date"}), 400

    # Query WFH request dates within the date range for the given staff_id
    wfh_dates = WFHRequestDates.query.filter(
        WFHRequestDates.staff_id == staff_id,
        WFHRequestDates.specific_date >= start_date,
        WFHRequestDates.specific_date <= end_date
    ).all()

    if not wfh_dates:
        return jsonify({"message": "No WFH dates found for this staff member in the given date range"}), 404

    return jsonify([date.json() for date in wfh_dates])

# Get all wfh dates and in office dates for a certain staff id in a certain date range
#GET /api/staff/1/wfh_office_dates?start_date=2024-09-01&end_date=2024-09-30
# {
#   "wfh_dates": [
#     {
#       "date_id": 2,
#       "request_id": 2,
#       "staff_id": 1,
#       "specific_date": "2024-09-02",
#       "is_am": true,
#       "is_pm": false
#     }
#   ],
#   "in_office_dates": [
#     {
#       "date": "2024-09-01",
#       "is_am": true,
#       "is_pm": true
#     }
#   ]
# }

@main.route("/api/staff/<int:staff_id>/wfh_office_dates", methods=["GET"])
def get_staff_wfh_and_office_dates_in_range(staff_id):
    start_date = request.args.get('start_date')
    end_date = request.args.get('end_date')

    if not start_date or not end_date:
        return jsonify({"error": "Please provide both start_date and end_date"}), 400

    # Convert string dates into datetime objects
    start = datetime.strptime(start_date, '%Y-%m-%d')
    end = datetime.strptime(end_date, '%Y-%m-%d')

    # Get all dates within the range
    def get_date_range(start, end):
        delta = end - start  # timedelta object
        return [start + timedelta(days=i) for i in range(delta.days + 1)]

    # Get the list of all dates in the range
    all_dates = get_date_range(start, end)

    # Query WFH request dates within the date range for the given staff_id
    wfh_dates = WFHRequestDates.query.filter(
        WFHRequestDates.staff_id == staff_id,
        WFHRequestDates.specific_date >= start_date,
        WFHRequestDates.specific_date <= end_date
    ).all()

    # Prepare a dictionary to store WFH status by date
    wfh_dict = {}
    for wfh in wfh_dates:
        date_str = str(wfh.specific_date)
        wfh_dict[date_str] = {
            "is_am": wfh.is_am,
            "is_pm": wfh.is_pm
        }

    # Prepare the in-office logic
    in_office_days = []
    for day in all_dates:
        date_str = str(day.date())

        if date_str in wfh_dict:
            # If there is a WFH entry for this date
            in_office_am = not wfh_dict[date_str]["is_am"]
            in_office_pm = not wfh_dict[date_str]["is_pm"]
        else:
            # If no WFH, they are in-office for the whole day
            in_office_am = True
            in_office_pm = True

        in_office_days.append({
            "date": date_str,
            "is_am": in_office_am,
            "is_pm": in_office_pm
        })

    return jsonify({
        "wfh_dates": [wfh.json() for wfh in wfh_dates],
        "in_office_dates": in_office_days
    })


##THIS CHECKS THE NAMES OF THE TABLES IN THE DB
@main.route("/api/check-tables", methods=['GET'])
def check_tables():
    # Use the inspector to get a list of tables
    inspector = inspect(db.engine)
    tables = inspector.get_table_names()
    return jsonify({"tables": tables})

##### STAFF APPLY #####

@main.route("/api/apply", methods=['POST'])
def apply():

    data = request.get_json()
    if not data:
        return jsonify({"error": "Invalid JSON or no data provided"}), 400
    
    if data.get("request_type") == "Ad-hoc":
        return handle_adhoc_request(data)
    
    elif data.get("request_type") == "Recurring":
        pass
        # Not implemented yet
        # return handle_recurring_request(data)
    else:
        return jsonify({"error": "Invalid request type"}), 400
    
    


    