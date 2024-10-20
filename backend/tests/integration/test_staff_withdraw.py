import unittest
from unittest.mock import patch
from datetime import date
import flask_testing
import json
from server import app, db
from models import *

class TestApp(flask_testing.TestCase):
    app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite://"
    app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {}
    app.config['TESTING'] = True

    def create_app(self):
        return app

    def setUp(self):
        db.create_all()
        employee = Employee(
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

        manager = Employee(
            staff_id=140001,
            staff_fname="Derek",
            staff_lname="Tan",
            dept="Sales",
            position="Director",
            country="Singapore",
            email="Derek.Tan@allinone.com.sg",
            reporting_manager=130002,
            role=1
        )

        wfh_request = WFHRequests(
            request_id="1",
            staff_id=140008,
            manager_id=140001,
            specific_date=date(2024, 9, 15),
            is_am=True,
            is_pm=True,
            request_status='Approved',
            apply_date=date(2024, 9, 10),
            request_reason='Personal matters'
        )

        db.session.add(employee)
        db.session.add(manager)
        db.session.add(wfh_request)
        db.session.commit()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

class TestStaffWithdraw(TestApp):
    def test_staff_withdraw_invalid_json(self):
        request_body = {}

        response = self.client.post("/api/withdraw",
                                    data=json.dumps(request_body),
                                    content_type='application/json')
        
        self.assertEqual(response.get_json(), {"error": "Invalid JSON or no data provided"})

    def test_staff_withdraw_missing_field(self):
        request_body = {
            'reason': 'Applied for the wrong day',
            'specific_date': "2024-09-15",
        }

        response = self.client.post("/api/withdraw",
                                    data=json.dumps(request_body),
                                    content_type='application/json')
        
        self.assertEqual(response.get_json(), {"error": "Missing 'request_id' in request"})

    def test_staff_withdraw_invalid_request(self):
        request_body = {
            'request_id': "0",
            'reason': 'Applied for the wrong day',
            'specific_date': "2024-09-15",
        }

        response = self.client.post("/api/withdraw",
                                    data=json.dumps(request_body),
                                    content_type='application/json')
        
        self.assertEqual(response.get_json(), {"error": "Request not found"})

    def test_staff_withdraw_not_approved(self):
        wfh_request = WFHRequests(
            request_id="2",
            staff_id=140008,
            manager_id=140001,
            specific_date=date(2024, 9, 18),
            is_am=True,
            is_pm=True,
            request_status='Pending',
            apply_date=date(2024, 9, 10),
            request_reason='Personal matters again'
        )
        db.session.add(wfh_request)
        db.session.commit()

        request_body = {
            'request_id': "2",
            'reason': 'Applied for the wrong day',
            'specific_date': "2024-09-18",
        }

        response = self.client.post("/api/withdraw",
                                    data=json.dumps(request_body),
                                    content_type='application/json')
        
        self.assertEqual(response.get_json(), {"error": "Request has not been approved."})

    @patch('util.wfh_requests.date')        
    def test_staff_withdraw_success(self, mock_date):
        mock_date.fromisoformat.return_value = date(2024, 12, 12)

        request_body = {
            'request_id': "1",
            'reason': 'Applied for the wrong day',
            'specific_date': "2024-09-15",
        }

        response = self.client.post("/api/withdraw",
                                    data=json.dumps(request_body),
                                    content_type='application/json')
        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_json()["message"], "Withdraw request successfully created.")
        self.assertEqual(response.get_json()["request"], {
            'request_id': "1",
            'staff_id': 140008,
            'manager_id': 140001,
            'specific_date': "2024-09-15",
            'is_am': True,
            'is_pm': True,
            "request_status": "Pending_Withdraw",
            'apply_date': "2024-12-12",
            'request_reason': "Applied for the wrong day"
            })


