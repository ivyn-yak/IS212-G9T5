from datetime import date
from models import *

def create_withdraw_decision(data):
    try: 
        decision = WithdrawDecisions(
                request_id=data["request_id"],
                specific_date = date.isoformat(data["specific_date"]),
                manager_id=data["manager_id"],
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