from models import *
from datetime import date, datetime

def get_request(request_id, specific_date):
    wfh_request = WFHRequests.query.filter_by(request_id=request_id, specific_date=specific_date).first()
    if not wfh_request:
        return None
    return wfh_request.json()

def get_request_by_id(request_id):
    wfh_request = WFHRequests.query.filter_by(request_id=request_id).first()
    if not wfh_request:
        return None
    return wfh_request.json()

def check_staff_request(staff_id, specific_date):
    wfh_request = WFHRequests.query.filter_by(staff_id=staff_id, specific_date=specific_date).first()
    if not wfh_request:
        return None
    return wfh_request.json()

def update_request(request_id, specific_date, data):
    try: 
        wfh_request = WFHRequests.query.filter_by(request_id=request_id, specific_date=specific_date).first()
        if not wfh_request:
            return None
        
        # decision can be approved, rejected, cancelled, withdrawn
        if 'manager_id' in data:
            wfh_request.manager_id = data['manager_id']
        if 'is_am' in data:
            wfh_request.is_am = data['is_am']
        if 'is_pm' in data:
            wfh_request.is_pm = data['is_pm']
        if 'request_status' in data:
            wfh_request.request_status = data['request_status']
        if 'apply_date' in data:
            wfh_request.apply_date = date.fromisoformat(data['apply_date'])
        if 'request_reason' in data:
            wfh_request.request_reason = data['request_reason']

        db.session.commit()

        return {"message": "Request updated", "new_request": wfh_request.json()}

    # new_request_log = WFHRequestLogs(
    #     log_datetime=datetime.now(),  
    #     request_id=wfh_request.request_id,
    #     specific_date=wfh_request.specific_date,
    #     request_status=wfh_request.request_status,  
    #     apply_log_date=wfh_request.apply_date,
    #     reason_log=wfh_request.request_reason
    # )

    # db.session.add(new_request_log)
    # db.session.commit()

    except Exception as e:
        db.session.rollback()
        return {"error": f"An error occurred: {str(e)}"}, 500


