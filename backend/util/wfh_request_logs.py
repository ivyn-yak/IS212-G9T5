from models import *
from datetime import datetime, date

def log_wfh_request(new_request):
    try:
        new_request_log = WFHRequestLogs(
            log_datetime=datetime.now(),
            request_id=new_request["request_id"],
            specific_date=date.fromisoformat(new_request["specific_date"]),
            request_status_log=new_request["request_status"],
            apply_date_log=date.fromisoformat(new_request["apply_date"]),
            reason_log=new_request["request_reason"]
        )

        db.session.add(new_request_log)
        db.session.commit()

        print(f"WFH request log added successfully for request ID: {new_request['request_id']}")

    except Exception as e:
        db.session.rollback()
        print(f"An error occurred while logging WFH request: {str(e)}")