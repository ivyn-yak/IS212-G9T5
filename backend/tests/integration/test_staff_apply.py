import unittest
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

        db.session.add(employee)
        db.session.add(manager)
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

    def test_staff_apply_adhoc(self):

        request_body = {
            'request_id' : 1,
            'staff_id': 140008,
            'request_type': 'Ad-hoc',
            'start_date': "2024-09-15",
            'end_date': "2024-09-15",
            'recurrence_days': None,
            'is_am': True,
            'is_pm': True,
            'apply_date': "2024-09-30",
            'request_reason': "Sick"
        }

        response = self.client.post("/api/apply",
                                    data=json.dumps(request_body),
                                    content_type='application/json')
        
        self.assertEqual(response.status_code, 201)
        # self.assertEqual(response.get_json(), {
        #     "message": "Ad-hoc request successfully created.",
        #     "request": {
        #         'request_id': 1,
        #         'staff_id': 140008,
        #         'manager_id': 140001,
        #         'request_type': 'Ad-hoc',
        #         'start_date': "2024-09-15",
        #         'end_date': "2024-09-15",
        #         'recurrence_days': None,
        #         'is_am': True,
        #         'is_pm': True,
        #         "request_status": "Pending",
        #         'apply_date': "2024-09-30",
        #         'withdraw_reason': None,
        #         'request_reason': "Sick"
        #         }
        #     })
        
#     def test_staff_apply_invalid_staff(self):
#         request_body = {
#             'staff_id': 0,
#             'request_type': 'Ad-hoc',
#             'start_date': "2024-09-15",
#             'end_date': "2024-09-15",
#             'recurrence_days': None,
#             'is_am': True,
#             'is_pm': True,
#             'apply_date': "2024-09-30",
#             'request_reason': "Sick"
#         }

#         response = self.client.post("/api/apply",
#                                     data=json.dumps(request_body),
#                                     content_type='application/json')
        
#         self.assertEqual(response.status_code, 404)
#         self.assertEqual(response.get_json(), {"error": "Staff not found"})

#     def test_staff_apply_invalid_request_type(self):
#         request_body = {
#             'staff_id': 140008,
#             'request_type': 'Wrong Type',
#             'start_date': "2024-09-15",
#             'end_date': "2024-09-15",
#             'recurrence_days': None,
#             'is_am': True,
#             'is_pm': True,
#             'apply_date': "2024-09-30",
#             'request_reason': "Sick"
#         }

#         response = self.client.post("/api/apply",
#                                     data=json.dumps(request_body),
#                                     content_type='application/json')
        
#         self.assertEqual(response.status_code, 400)
#         self.assertEqual(response.get_json(), {"error": "Invalid request type"})

#     def test_staff_apply_recurring_invalid_json(self):
#             request_body = {}

#             response = self.client.post("/api/apply",
#                                         data=json.dumps(request_body),
#                                         content_type='application/json')

#             self.assertEqual(response.status_code, 400)
#             self.assertEqual(response.get_json(), {"error": "Invalid JSON or no data provided"})

    def test_staff_apply_recurring(self):
            # Valid recurring request
            request_body = {
                'request_id' : 1,
                'staff_id': 140008,
                'request_type': 'Recurring',
                'start_date': "2024-09-15",
                'end_date': "2024-09-29",
                'recurrence_days': 'Monday',  # Recurring on Mondays and Wednesdays
                'is_am': True,
                'is_pm': False,
                'apply_date': "2024-09-01",
                'request_reason': "Regular remote work"
            }

            response = self.client.post("/api/apply",
                                        data=json.dumps(request_body),
                                        content_type='application/json')

            self.assertEqual(response.status_code, 201)
            response_json = response.get_json()
            self.assertEqual(response.get_json()["message"], "Recurring requests successfully created.")
            self.assertEqual(len(response_json["requests"]), 2)
            for req in response_json["requests"]:
                self.assertEqual(req["staff_id"], 140008)
                self.assertEqual(req["is_am"], True)
                self.assertEqual(req["is_pm"], False)
                self.assertEqual(req["request_status"], "Pending")


    def test_staff_apply_recurring_invalid_staff(self):
        # Invalid staff ID
        request_body = {
            'staff_id': 9999,  # Non-existent staff
            'request_type': 'Recurring',
            'start_date': "2024-09-15",
            'end_date': "2024-09-29",
            'recurrence_days': "Wednesday",  
            'is_am': True,
            'is_pm': False,
            'apply_date': "2024-09-01",
            'request_reason': "Regular remote work"
        }

        response = self.client.post("/api/apply",
                                    data=json.dumps(request_body),
                                    content_type='application/json')

        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.get_json(), {"error": "Staff not found"})
    
    def test_staff_apply_recurring_no_recurrence_days(self):
        # Missing recurrence days
        request_body = {
            'staff_id': 140008,
            'request_type': 'Recurring',
            'start_date': "2024-09-15",
            'end_date': "2024-09-29",
            'recurrence_days': None,  # Missing recurrence days
            'is_am': True,
            'is_pm': False,
            'apply_date': "2024-09-01",
            'request_reason': "Regular remote work"
        }

        response = self.client.post("/api/apply",
                                    data=json.dumps(request_body),
                                    content_type='application/json')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.get_json(), {"error": "Recurrence days not provided"})

    def test_staff_apply_recurring_invalid_request_type(self):
        # Invalid request type
        request_body = {
            'staff_id': 140008,
            'request_type': 'Wrong Type',
            'start_date': "2024-09-15",
            'end_date': "2024-09-29",
            'recurrence_days': [0, 2],  
            'is_am': True,
            'is_pm': False,
            'apply_date': "2024-09-01",
            'request_reason': "Regular remote work"
        }

        response = self.client.post("/api/apply",
                                    data=json.dumps(request_body),
                                    content_type='application/json')

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.get_json(), {"error": "Invalid request type"})

if __name__ == '__main__':
    unittest.main()

