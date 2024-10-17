import unittest
import flask_testing
import json
from datetime import datetime, date
# from backend import server
from server import app, db
from models import *
from datetime import timedelta

class TestApp(flask_testing.TestCase):
    app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite://"
    app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {}
    app.config['TESTING'] = True

    def create_app(self):
        return app

    def setUp(self):
        db.create_all()

        self.manager = Employee(
            staff_id=140001,
            staff_fname="Derek",
            staff_lname="Tan",
            dept="Sales",
            position="Director",
            country="Singapore",
            email="Derek.Tan@allinone.com.sg",
            reporting_manager=None,
            role=1
        )
        self.employee_1 = Employee(
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
        self.employee_2 = Employee(
            staff_id=140009,
            staff_fname="John",
            staff_lname="Doe",
            dept="Sales",
            position="Sales Associate",
            country="Singapore",
            email="John.Doe@allinone.com.sg",
            reporting_manager=140001,
            role=3
        )
        self.employee_3=Employee(
            staff_id=140010, 
            staff_fname='Sophia', 
            staff_lname='Toh', 
            dept='Sales', 
            position="Sales Manager", 
            country="Singapore",
            email="Sophia.Toh@allinone.com.sg",
            reporting_manager=140001,
            role=3
        )
        self.employee_4=Employee(
            staff_id=140011,
            staff_fname='Joseph',
            staff_lname='Tan',
            dept='Sales',
            position="Sales Manager", 
            country="Singapore",
            email="josephtan@allinone.come.sg",
            reporting_manager=140001,
            role=3
        )


        db.session.add(self.manager)
        db.session.add(self.employee_1)
        db.session.add(self.employee_2)
        db.session.add(self.employee_3)
        db.session.add(self.employee_4)
        db.session.commit()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

class TestManagerApproveRecurring(TestApp):

    def test_approve_recurring_invalid_json(self):
        request_body = {}
        response = self.client.post("/api/approve_recurring",
                                     data=json.dumps(request_body),
                                     content_type='application/json')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.get_json(), {"error": "Invalid JSON or no data provided"})

    def test_approve_recurring_request_not_found(self):
        request_body = {
            'request_id': 999
        }
        response = self.client.post("/api/approve_recurring",
                                     data=json.dumps(request_body),
                                     content_type='application/json')
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.get_json(), {"error": "Request not found"})


# not working 
    # def test_approve_recurring_employee_not_found(self):

    #     start_date = datetime.strptime("2024-09-15", '%Y-%m-%d')
    #     end_date = datetime.strptime("2024-09-30", '%Y-%m-%d')
        
    #     req = WFHRequests(
    #         request_id=1,
    #         staff_id=140010,  # Non-existing employee
    #         manager_id=140001,
    #         request_type='Recurring',
    #         start_date=datetime.strptime("2024-09-15", '%Y-%m-%d'),
    #         end_date=datetime.strptime("2024-09-30", '%Y-%m-%d'),
    #         recurrence_days='monday',
    #         request_status='Pending', 
    #         apply_date=date.today(), 
    #         withdrawable_until=start_date - timedelta(days=30)
    #     )
    #     db.session.add(req)
    #     db.session.commit()

    #     request_body = {
    #         'request_id': 1
    #     }
    #     response = self.client.post("/api/approve-recurring",
    #                                 data=json.dumps(request_body),
    #                                 content_type='application/json')
    #     self.assertEqual(response.status_code, 404)
    #     self.assertEqual(response.get_json(), {"error": "Employee with staff_id 140010 not found"})

    def test_approve_recurring_invalid_recurrence_day(self):

        start_date = datetime.strptime("2024-09-15", '%Y-%m-%d')
        end_date = datetime.strptime("2024-09-30", '%Y-%m-%d')


        req = WFHRequests(
            request_id=2,
            staff_id=140008,
            manager_id=140001,
            request_type='Recurring',
            start_date=datetime.strptime("2024-09-15", '%Y-%m-%d'),
            end_date=datetime.strptime("2024-09-30", '%Y-%m-%d'),
            recurrence_days='invalid_day',
            request_status='Pending',
            apply_date=date.today(), 
            withdraw_reason=None
        )
        db.session.add(req)
        db.session.commit()

        request_body = {
            'request_id': 2
        }
        response = self.client.post("/api/approve_recurring",
                                    data=json.dumps(request_body),
                                    content_type='application/json')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.get_json(), {"error": "Invalid recurrence day format"})

    def test_approve_recurring_success(self):

        start_date = datetime.strptime("2024-09-15", '%Y-%m-%d')
        end_date = datetime.strptime("2024-09-30", '%Y-%m-%d')

        req = WFHRequests(
            request_id=3,
            staff_id=140008,
            manager_id=140001,
            request_type='Recurring',
            start_date=datetime.strptime("2024-09-15", '%Y-%m-%d'),
            end_date=datetime.strptime("2024-09-30", '%Y-%m-%d'),
            recurrence_days='monday',
            request_status='Pending',
            apply_date=date.today(), 
            withdraw_reason=None
 
        )
        db.session.add(req)
        db.session.commit()

        request_body = {
            'request_id': 3,
            'decision_status':'Approved', 
            'decision_notes': 'Nil', 
            'manager_id': 14001

        }
        response = self.client.post("/api/approve_recurring",
                                    data=json.dumps(request_body),
                                    content_type='application/json')

        if response.status_code != 201:
            print("Response Data:", response.get_json()) 

        self.assertEqual(response.status_code, 201)
        self.assertIn("Recurring WFH requests processed successfully", response.get_json()["message"])

    def test_approve_recurring_headcount_exceed(self):
        wfh_request_1 = WFHRequests(
            request_id=1,
            staff_id=140008,
            manager_id=140001,
            request_type='Ad-hoc',
            start_date=datetime.strptime("2024-09-16", '%Y-%m-%d'),
            end_date=datetime.strptime("2024-09-20", '%Y-%m-%d'),
            request_status='Approved',
            apply_date=datetime.now(),
            withdraw_reason=datetime.strptime("2024-09-10", '%Y-%m-%d'),
            request_reason='Personal matters',
            is_am=False,
            is_pm=True
        )
        db.session.add(wfh_request_1)

        wfh_request_2 = WFHRequests(
            request_id=3,
            staff_id=140010,
            manager_id=140001,
            request_type='Ad-hoc',
            start_date=datetime.strptime("2024-09-16", '%Y-%m-%d'),
            end_date=datetime.strptime("2024-09-20", '%Y-%m-%d'),
            request_status='Approved',
            apply_date=datetime.now(),
            withdraw_reason=datetime.strptime("2024-09-10", '%Y-%m-%d'),
            request_reason='Personal matters',
            is_am=False,
            is_pm=True
        )
        db.session.add(wfh_request_2)

        wfh_request_3 = WFHRequests(
            request_id=2,
            staff_id=140009,
            manager_id=140001,
            request_type='Recurring',
            start_date=datetime.strptime("2024-09-16", '%Y-%m-%d'),
            end_date=datetime.strptime("2024-09-20", '%Y-%m-%d'),
            recurrence_days='monday',
            request_status='Pending',
            apply_date=datetime.now(),
            withdraw_reason=datetime.strptime("2024-09-10", '%Y-%m-%d'),
            request_reason='Personal matters',
            is_am=False,
            is_pm=True
        )
        db.session.add(wfh_request_3)

        wfh_request_date_1 = WFHRequestDates(
                request_id = 1, 
                specific_date=datetime.strptime("2024-09-16", '%Y-%m-%d'),
                decision_status='Approved',
                staff_id=140008,
                is_am=False,
                is_pm=True
            )
        db.session.add(wfh_request_date_1)

        wfh_request_date_2 = WFHRequestDates(
                request_id = 3, 
                specific_date=datetime.strptime("2024-09-16", '%Y-%m-%d'),
                decision_status='Approved',
                staff_id=140010,
                is_am=False,
                is_pm=True
            )
        db.session.add(wfh_request_date_2)
        db.session.commit()

        request_body = {
            'request_id': 2,
            'decision_status': 'Approved',
            'start_date': '2024-09-16',  
            'decision_notes': 'Nil',
            'manager_id': 140001
        }

        response = self.client.post("/api/approve_recurring",
                                    data=json.dumps(request_body),
                                    content_type='application/json')
        
        self.assertEqual(response.status_code, 422)
        self.assertEqual(response.get_json(), {"error": "Exceed 0.5 rule limit for PM session"})

if __name__ == "__main__":
    unittest.main()
