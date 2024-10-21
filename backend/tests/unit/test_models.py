import unittest
from unittest.mock import patch
from models import *
import datetime
import uuid

class TestEmployee(unittest.TestCase):
    def test_json(self):
        new_employee = Employee(
            staff_id=140008,
            staff_fname="Jaclyn",
            staff_lname="Lee",
            dept="Sales",
            position="Sales Manager",
            country="Singapore",
            email="Jaclyn.Lee@allinone.com.sg",
            reporting_manager=140001,
            role=3
        )
        
        self.assertEqual(new_employee.json(), {
        "country": "Singapore",
        "dept": "Sales",
        "email": "Jaclyn.Lee@allinone.com.sg",
        "position": "Sales Manager",
        "reporting_manager": 140001,
        "role": 3,
        "staff_fname": "Jaclyn",
        "staff_id": 140008,
        "staff_lname": "Lee"
        })

class TestWFHRequests(unittest.TestCase):
    def test_json(self):
        req = WFHRequests(
            request_id="1",
            staff_id=140008,
            manager_id=140001,
            specific_date=datetime.date(2024, 9, 15),  
            is_am=True,
            is_pm=True, 
            request_status= "Pending",  
            apply_date=datetime.date(2024, 9, 30),
            request_reason="Sick"
            )

        self.assertEqual(req.json(), {
            'request_id': '1',
            'staff_id': 140008,
            'manager_id': 140001,
            'specific_date': "2024-09-15",
            'is_am': True,
            'is_pm': True,
            "request_status": "Pending",
            'apply_date': "2024-09-30",
            'request_reason': "Sick"
        })

class TestWFHRequestLogs(unittest.TestCase):
    def test_json(self):
        date = WFHRequestLogs(
            log_datetime=datetime.datetime(2024, 12, 12, 0, 30, 0),
            request_id="1", 
            specific_date=datetime.date(2024, 9, 15),
            request_status="Approved",
            apply_log_date=datetime.date(2024, 9, 18),
            reason_log="Tired"
            )
        
        self.assertEqual(date.json(), {
            "log_datetime": "2024-12-12 00:30:00",
            "request_id": "1",
            "specific_date": "2024-09-15",
            "request_status": "Approved",
            "apply_log_date": "2024-09-18",
            "reason_log": "Tired"
        })

class TestRequestDecisions(unittest.TestCase):
    def test_json(self):
        decision = RequestDecisions(
            decision_id=1,
            request_id="1",
            manager_id=140001,
            decision_status="Approved",
            decision_date=datetime.date(2024, 12, 12),
            decision_notes="Ok"
            )
        
        self.assertEqual(decision.json(), {
            "decision_id": 1,
            "request_id": "1",
            "manager_id": 140001,
            "decision_date": "2024-12-12",
            "decision_status": "Approved",
            "decision_notes": "Ok"
        })

class TestWithdrawDecisions(unittest.TestCase):
    def test_json(self):
        decision = WithdrawDecisions(
            withdraw_decision_id=1,
            specific_date=datetime.date(2024, 9, 15),
            request_id="1",
            manager_id=140001,
            decision_status="Approved",
            decision_date=datetime.date(2024, 12, 12),
            decision_notes="Ok"
            )
        
        self.assertEqual(decision.json(), {
            "withdraw_decision_id": 1,
            "specific_date": "2024-09-15",
            "request_id": "1",
            "manager_id": 140001,
            "decision_date": "2024-12-12",
            "decision_status": "Approved",
            "decision_notes": "Ok"
        })


if __name__ == "__main__":
    unittest.main()
