import datetime
from models import *

def create_request_decision(data):
    try: 
        decision = RequestDecisions(
                request_id=data["request_id"],
                manager_id=data.get("manager_id"),
                decision_status=data["decision_status"],
                decision_date = datetime.today().date(),
                decision_notes=data["decision_notes"]
            )

        db.session.add(decision)
        db.session.commit()

        return {
            "message": "Manager's request decision successfully created.",
            "decision": decision.json()
        }
        
    except Exception as e:
        db.session.rollback()
        return {"error": str(e)}