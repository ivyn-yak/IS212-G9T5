from datetime import datetime
from models import *

def add_approved_date(request):
    try: 
        specific_date = datetime.strptime(request["start_date"], '%Y-%m-%d')
        new_date = WFHRequestDates(
            request_id=request["request_id"],
            specific_date=specific_date,
            staff_id=request["staff_id"],
            is_am=request["is_am"],
            is_pm=request["is_pm"]
            )
        
        db.session.add(new_date)
        db.session.commit()

        return {"message": "WFH date successfully added!", "wfh_date": new_date.json()}

    except Exception as e:
        db.session.rollback()
        return {"error": str(e)}