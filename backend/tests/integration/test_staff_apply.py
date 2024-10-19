import unittest
from unittest.mock import patch
import datetime
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
            request_id = "1",
            staff_id=140008,
            manager_id=140001,
            specific_date=datetime.date(2024, 9, 20),
            is_am=True,
            is_pm=True,
            request_status='Pending',
            apply_date=datetime.date(2024, 9, 30),
            request_reason="Sick"
        )

        db.session.add(employee)
        db.session.add(manager)
        db.session.add(wfh_request)
        db.session.commit()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

class TestStaffApply(TestApp):
    def test_staff_apply_adhoc_invalid_json(self):
        request_body = {}

        response = self.client.post("/api/apply",
                                    data=json.dumps(request_body),
                                    content_type='application/json')
        
        self.assertEqual(response.get_json(), {"error": "Invalid JSON or no data provided"})

    @patch('util.staff_apply.uuid.uuid4')
    def test_staff_apply_adhoc(self, mock_uuid):
        mock_uuid.return_value = uuid.UUID('12345678-1234-5678-1234-567812345678')

        request_body = {
            'staff_id': 140008,
            'request_type': 'Ad-hoc',
            'specific_date': "2024-09-15",
            'is_am': True,
            'is_pm': True,
            'apply_date': "2024-09-30",
            'request_reason': "Sick"
        }

        response = self.client.post("/api/apply",
                                    data=json.dumps(request_body),
                                    content_type='application/json')
                
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.get_json(), {
            "message": "Ad-hoc request successfully created.",
            "request": {
                'request_id': '12345678-1234-5678-1234-567812345678',
                'staff_id': 140008,
                'manager_id': 140001,
                'specific_date': "2024-09-15",
                'is_am': True,
                'is_pm': True,
                "request_status": "Pending",
                'apply_date': "2024-09-30",
                'request_reason': "Sick"
                }
            })
        
    def test_staff_apply_invalid_staff(self):
        request_body = {
            'staff_id': 0,
            'request_type': 'Ad-hoc',
            'specific_date': "2024-09-15",
            'is_am': True,
            'is_pm': True,
            'apply_date': "2024-09-30",
            'request_reason': "Sick"
        }

        response = self.client.post("/api/apply",
                                    data=json.dumps(request_body),
                                    content_type='application/json')
        
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.get_json(), {"error": "Staff not found"})

    def test_staff_apply_invalid_request_type(self):
        request_body = {
            'staff_id': 140008,
            'request_type': 'Wrong Type',
            'specific_date': "2024-09-15",
            'is_am': True,
            'is_pm': True,
            'apply_date': "2024-09-30",
            'request_reason': "Sick"
        }

        response = self.client.post("/api/apply",
                                    data=json.dumps(request_body),
                                    content_type='application/json')
        
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.get_json(), {"error": "Invalid request type"})

    def test_staff_apply_existing_request(self):
        request_body = {
            'staff_id': 140008,
            'request_type': 'Ad-hoc',
            'specific_date': "2024-09-20",
            'is_am': True,
            'is_pm': True,
            'apply_date': "2024-09-30",
            'request_reason': "Sick"
        }

        response = self.client.post("/api/apply",
                                    data=json.dumps(request_body),
                                    content_type='application/json')
        
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.get_json(), {"error": f"Staff has an existing request for 2024-09-20"})

#     def test_staff_apply_recurring_invalid_json(self):
#             request_body = {}

#             response = self.client.post("/api/apply",
#                                         data=json.dumps(request_body),
#                                         content_type='application/json')

#             self.assertEqual(response.status_code, 400)
#             self.assertEqual(response.get_json(), {"error": "Invalid JSON or no data provided"})

#     def test_staff_apply_recurring(self):
#             # Valid recurring request
#             request_body = {
#                 'staff_id': 140008,
#                 'request_type': 'Recurring',
#                 'start_date': "2024-09-15",
#                 'end_date': "2024-09-29",
#                 'recurrence_days': 'Monday',  # Recurring on Mondays and Wednesdays
#                 'is_am': True,
#                 'is_pm': False,
#                 'apply_date': "2024-09-01",
#                 'request_reason': "Regular remote work"
#             }

#             response = self.client.post("/api/apply",
#                                         data=json.dumps(request_body),
#                                         content_type='application/json')

#             self.assertEqual(response.status_code, 201)
#             self.assertEqual(response.get_json()["message"], "Recurring request successfully created.")

#     def test_staff_apply_recurring_invalid_staff(self):
#         # Invalid staff ID
#         request_body = {
#             'staff_id': 9999,  # Non-existent staff
#             'request_type': 'Recurring',
#             'start_date': "2024-09-15",
#             'end_date': "2024-09-29",
#             'recurrence_days': "Wednesday",  
#             'is_am': True,
#             'is_pm': False,
#             'apply_date': "2024-09-01",
#             'request_reason': "Regular remote work"
#         }

#         response = self.client.post("/api/apply",
#                                     data=json.dumps(request_body),
#                                     content_type='application/json')

#         self.assertEqual(response.status_code, 404)
#         self.assertEqual(response.get_json(), {"error": "Staff not found"})
    
#     def test_staff_apply_recurring_no_recurrence_days(self):
#         # Missing recurrence days
#         request_body = {
#             'staff_id': 140008,
#             'request_type': 'Recurring',
#             'start_date': "2024-09-15",
#             'end_date': "2024-09-29",
#             'recurrence_days': None,  # Missing recurrence days
#             'is_am': True,
#             'is_pm': False,
#             'apply_date': "2024-09-01",
#             'request_reason': "Regular remote work"
#         }

#         response = self.client.post("/api/apply",
#                                     data=json.dumps(request_body),
#                                     content_type='application/json')

#         self.assertEqual(response.status_code, 400)
#         self.assertEqual(response.get_json(), {"error": "Recurrence days not provided"})

#     def test_staff_apply_recurring_invalid_request_type(self):
#         # Invalid request type
#         request_body = {
#             'staff_id': 140008,
#             'request_type': 'Wrong Type',
#             'start_date': "2024-09-15",
#             'end_date': "2024-09-29",
#             'recurrence_days': [0, 2],  
#             'is_am': True,
#             'is_pm': False,
#             'apply_date': "2024-09-01",
#             'request_reason': "Regular remote work"
#         }

#         response = self.client.post("/api/apply",
#                                     data=json.dumps(request_body),
#                                     content_type='application/json')

#         self.assertEqual(response.status_code, 400)
#         self.assertEqual(response.get_json(), {"error": "Invalid request type"})

if __name__ == '__main__':
    unittest.main()

