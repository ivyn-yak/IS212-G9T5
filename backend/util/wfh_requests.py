from models import *

def get_request(request_id):
    wfh_request = WFHRequests.query.filter_by(request_id=request_id).first()
    if not wfh_request:
        return None
    return wfh_request.json()

def update_request(request_id, data):
    wfh_request = get_request(request_id)
    if not wfh_request:
        return None
    
    # decision can be approved, rejected, cancelled, withdrawn
    if 'start_date' in data:
        wfh_request['start_date'] = data['start_date']
    if 'end_date' in data:
        wfh_request['end_date'] = data['end_date']
    if 'recurrence_days' in data:
        wfh_request['recurrence_days'] = data['recurrence_days']
    if 'is_am' in data:
        wfh_request['is_am'] = data['is_am']
    if 'is_pm' in data:
        wfh_request['is_pm'] = data['is_pm']
    if 'request_status' in data:
        wfh_request['request_status'] = data['request_status']
    if 'request_reason' in data:
        wfh_request['request_reason'] = data['request_reason']

    db.session.commit()

    return {"message": "Request updated", "new_request": wfh_request}


