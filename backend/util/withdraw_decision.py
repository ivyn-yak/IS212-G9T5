from datetime import datetime
from models import *

def create_withdraw_decision(data):
    try:
        decision_date = datetime.now()
        new_decision = WithdrawDecisions(
            request_id=data["request_id"],
            specific_date=data["specific_date"],
            manager_id=data["manager_id"],
            decision_date=data["decision_date"],
            decision_status=data["decision_status"],
            decision_notes=data["decision_notes"]
        )
        
        db.session.add(new_decision)
        db.session.commit()
        
        return {
            "withdraw_decision_id": new_decision.withdraw_decision_id,
            "request_id": data["request_id"],
            "specific_date": data["specific_date"],
            "manager_id": data["manager_id"],
            "decision_date": data["decision_date"],
            "decision_status": data["decision_status"],
            "decision_notes": data["decision_notes"]
        }
    except Exception as e:
        db.session.rollback()
        return {"error": f"Failed to store decision: {str(e)}"}
