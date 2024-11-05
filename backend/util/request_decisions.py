from datetime import date
from models import *

def create_request_decision(data):
    try: 
        decision = RequestDecisions(
            request_id=data["request_id"],
            manager_id=data["manager_id"],
            specific_date = data["specific_date"],
            decision_status=data["decision_status"],
            decision_date = date.today(),
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