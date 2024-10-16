from flask import Blueprint, jsonify, request
from models import *
from datetime import datetime, timedelta
from util.employee import get_full_team, get_employee_by_id


dates = Blueprint('dates', __name__)

##### WFHREQUESTDATES TABLE #####
# Get all wfh dates for a certain staff id
# GET /api/staff/1/wfh_dates
# [
#   {
#     "date_id": 1,
#     "request_id": 1,
#     "staff_id": 1,
#     "decision_status": "Approved",
#     "specific_date": "2024-09-24",
#     "is_am": true,
#     "is_pm": true
#   }
# ]
@dates.route("/api/staff/<int:staff_id>/all_wfh_dates", methods=["GET"])
def get_staff_wfh_dates(staff_id):

    wfh_dates = WFHRequestDates.query.filter_by(staff_id=staff_id).all()

    if not wfh_dates:
        return jsonify({"message": "No WFH dates found for this staff member"}), 404

    return jsonify([date.json() for date in wfh_dates])

# Get all wfh dates for a certain staff id in a certain date range
#GET /api/staff/1/wfh_dates_in_range?start_date=2024-09-01&end_date=2024-09-30
# [
#   {
#     "date_id": 2,
#     "request_id": 2,
#     "staff_id": 1,
#     "decision_status": "Approved",
#     "specific_date": "2024-09-02",
#     "is_am": true,
#     "is_pm": false
#   }
# ]

@dates.route("/api/staff/<int:staff_id>/wfh_dates_in_range", methods=["GET"])
def get_staff_wfh_dates_in_range(staff_id):
    start_date = request.args.get('start_date')
    end_date = request.args.get('end_date')

    if not start_date or not end_date:
        return jsonify({"error": "Please provide both start_date and end_date"}), 400

    # Query WFH request dates within the date range for the given staff_id
    wfh_dates = WFHRequestDates.query.filter(
        WFHRequestDates.staff_id == staff_id,
        WFHRequestDates.specific_date >= start_date,
        WFHRequestDates.specific_date <= end_date,
        WFHRequestDates.decision_status == "Approved"
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
#       "decision_status": "Approved",
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

@dates.route("/api/staff/<int:staff_id>/wfh_office_dates", methods=["GET"])
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
        WFHRequestDates.specific_date <= end_date,
        WFHRequestDates.decision_status == "Approved"
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

# Get the WFH schedule for a staff member and their team for a given week
# GET /api/staff/<int:staff_id>/team_wfh_schedule?start_week_date=2024-09-01
@dates.route("/api/staff/<int:staff_id>/team_wfh_schedule", methods=["GET"])
def get_staff_and_team_wfh_schedule(staff_id):
    start_week_date = request.args.get('start_week_date')
    if not start_week_date:
        return jsonify({"error": "Please provide start_week_date"}), 400

    # Calculate end date (7 days after start)
    start_date = datetime.strptime(start_week_date, '%Y-%m-%d')
    end_date = start_date + timedelta(days=6)

    # Get the staff and their team
    employee = get_employee_by_id(staff_id)
    if not employee:  # Check if employee exists
        return jsonify({"error": "Employee not found"}), 404

    # Manually extract properties from the returned dictionary
    reporting_manager = employee.get("reporting_manager")
    role = employee.get("role")

    # Determine the correct staff ID for full_team based on role
    full_team = get_full_team(reporting_manager if role == 2 else staff_id)

    # Prepare the response structure
    schedule_response = {"staff": {}, "team": []}

    # Function to get WFH dates for a staff member
    def get_wfh_schedule(staff_id):
        wfh_dates = WFHRequestDates.query.filter(
            WFHRequestDates.staff_id == staff_id,
            WFHRequestDates.specific_date >= start_date,
            WFHRequestDates.specific_date <= end_date
        ).all()

        # Return the dates in the desired format
        return [{"date": str(date.specific_date), "is_am": date.is_am, "is_pm": date.is_pm} for date in wfh_dates]

    # Get the schedule for the main staff
    schedule_response["staff"] = {
        "staffID": staff_id,
        "scheduleTrails": get_wfh_schedule(staff_id)
    }

    # Get the schedule for the team and include the name in the response
    for member in full_team:
        schedule_response["team"].append({
            "staffID": member.staff_id,
            "name": f"{member.staff_fname} {member.staff_lname}",
            "scheduleTrails": get_wfh_schedule(member.staff_id)
        })

    return jsonify(schedule_response)



# Get department schedules for a given week
# GET /api/departments/schedules?start_week_date=2024-09-01
@dates.route("/api/departments/schedules", methods=["GET"])
def get_department_schedules():
    start_week_date = request.args.get('start_week_date')
    if not start_week_date:
        return jsonify({"error": "Please provide start_week_date"}), 400
    
    start_date = datetime.strptime(start_week_date, '%Y-%m-%d')
    end_date = start_date + timedelta(days=6)

    # Query all departments
    departments = Employee.query.distinct(Employee.dept).all()
    department_response = []

    # Function to get WFH dates for a staff member
    def get_wfh_schedule(staff_id):
        wfh_dates = WFHRequestDates.query.filter(
            WFHRequestDates.staff_id == staff_id,
            WFHRequestDates.specific_date >= start_date,
            WFHRequestDates.specific_date <= end_date
        ).all()
        return [date.json() for date in wfh_dates]

    # Iterate through each department
    for department in departments:
        department_name = department.dept

        # Get all staff in the department
        department_staff = Employee.query.filter_by(dept=department_name).all()

        # Group staff by their teams
        teams_dict = {}
        for staff in department_staff:
            rm_id = staff.reporting_manager if staff.role == 2 else staff.staff_id
            if rm_id not in teams_dict:
                teams_dict[rm_id] = []

            teams_dict[rm_id].append(staff)

        # Prepare teams' schedules
        teams = []
        for rm_id, team_members in teams_dict.items():
            team_schedule = []
            for member in team_members:
                team_schedule.append({
                    "staff_id": member.staff_id,
                    "ScheduleDetails": get_wfh_schedule(member.staff_id)
                })
            teams.append(team_schedule)

        department_response.append({
            "department_name": department_name,
            "teams": teams
        })

    return jsonify(department_response)
