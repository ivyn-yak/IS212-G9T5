import unittest
from unittest.mock import patch
import flask_testing
import json
from datetime import datetime, date
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
        self.manager_2 = Employee(
            staff_id=140002,
            staff_fname="Jakobson",
            staff_lname="Tan",
            dept="HR",
            position="Director",
            country="Singapore",
            email="Jakobson@allinone.com.sg",
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
        db.session.add(self.manager_2)
        db.session.add(self.employee_1)
        db.session.add(self.employee_2)
        db.session.add(self.employee_3)
        db.session.add(self.employee_4)
        db.session.commit()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

class TestManagerApproveAdhoc(TestApp):

    def test_approve_adhoc_invalid_json(self):
        request_body = {}
        response = self.client.post("/api/approve",
                                     data=json.dumps(request_body),
                                     content_type='application/json')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.get_json(), {"error": "Invalid JSON or no data provided"})

    def test_approve_adhoc_missing_field(self):
        request_body = {
            'manager_id': "140001",
            "decision_notes": "Nil",
            'decision_status': 'Approved'
        }
        response = self.client.post("/api/approve",
                                     data=json.dumps(request_body),
                                     content_type='application/json')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.get_json(), {"error": f"Missing 'request_id' in request"})

    def test_approve_adhoc_request_not_found(self):
        request_body = {
            'request_id': "999", 
            'manager_id': "140001",
            "decision_notes": "Nil",
            'decision_status': 'Approved'
        }
        response = self.client.post("/api/approve",
                                     data=json.dumps(request_body),
                                     content_type='application/json')
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.get_json(), {"error": "Request not found"})

    def test_approve_adhoc_staff_not_found(self):
        bad_request = WFHRequests(
            request_id="1",
            staff_id=0,
            manager_id=140001,
            specific_date=date(2024, 9, 15),
            is_am=False,
            is_pm=True,
            request_status='Pending',
            apply_date=date(2024, 9, 10),
            request_reason='Personal matters'
        )

        db.session.add(bad_request)
        db.session.commit()

        request_body = {
            'request_id': "1", 
            'manager_id': "140001",
            "decision_notes": "Nil",
            'decision_status': 'Approved'
        }
        response = self.client.post("/api/approve",
                                     data=json.dumps(request_body),
                                     content_type='application/json')
        
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.get_json(), {"error": "Employee with staff_id 0 not found"})

    def test_approve_adhoc_rm_not_found(self):
        wfh_request = WFHRequests(
            request_id="1",
            staff_id=140008,
            manager_id=140001,
            specific_date=date(2024, 9, 15),
            is_am=False,
            is_pm=True,
            request_status='Pending',
            apply_date=date(2024, 9, 10),
            request_reason='Personal matters'
        )

        db.session.add(wfh_request)
        db.session.commit()

        request_body = {
            'request_id': "1", 
            'manager_id': "0",
            "decision_notes": "Nil",
            'decision_status': 'Approved'
        }
        response = self.client.post("/api/approve",
                                     data=json.dumps(request_body),
                                     content_type='application/json')
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.get_json(), {"error": "Reporting manager for employee 140008 not found"})

    def test_approve_adhoc_different_rm(self):
        wfh_request = WFHRequests(
            request_id="1",
            staff_id=140008,
            manager_id=140001,
            specific_date=date(2024, 9, 15),
            is_am=False,
            is_pm=True,
            request_status='Pending',
            apply_date=date(2024, 9, 10),
            request_reason='Personal matters'
        )

        db.session.add(wfh_request)
        db.session.commit()

        request_body = {
            'request_id': "1", 
            'manager_id': "140009",
            "decision_notes": "Nil",
            'decision_status': 'Approved'
        }
        response = self.client.post("/api/approve",
                                     data=json.dumps(request_body),
                                     content_type='application/json')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.get_json(), {"error": "Employee 140008 reports under 140001 instead of 140009"})

    def test_approve_adhoc_not_pending(self):
        wfh_request = WFHRequests(
            request_id="1",
            staff_id=140008,
            manager_id=140001,
            specific_date=date(2024, 9, 15),
            is_am=False,
            is_pm=True,
            request_status='Approved',
            apply_date=date(2024, 9, 10),
            request_reason='Personal matters'
        )

        db.session.add(wfh_request)
        db.session.commit()

        request_body = {
            'request_id': "1", 
            'manager_id': "140001",
            "decision_notes": "Nil",
            'decision_status': 'Approved'
        }
        response = self.client.post("/api/approve",
                                     data=json.dumps(request_body),
                                     content_type='application/json')
        
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.get_json(), {"error": "Manager cannot approve or reject request with Approved status"})

    @patch('util.request_decisions.date')
    def test_headcount_check_below_50_percent(self, mock_datetime):
        mock_datetime.today.return_value = date(2024, 12, 12)

        wfh_request_2 = WFHRequests(
            request_id="2",
            staff_id=140009,
            manager_id=140001,
            specific_date=date(2024, 9, 15),
            request_status='Pending',
            apply_date=date(2024, 9, 30),
            request_reason='Personal matters',
            is_am=False,
            is_pm=True
        )
        db.session.add(wfh_request_2)
        db.session.commit()

        request_body = {
            'request_id': "2",
            'decision_status': 'Approved',
            'decision_notes': 'Nil',
            'manager_id': "140001"
        }

        response = self.client.post("/api/approve",
                                    data=json.dumps(request_body),
                                    content_type='application/json')
                
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.get_json()["message"], "Request updated and manager's decision stored successfully")
        self.assertEqual(response.get_json()["request"], {
                'request_id': "2",
                'staff_id': 140009,
                'manager_id': 140001,
                'specific_date': "2024-09-15",
                'is_am': False,
                'is_pm': True,
                "request_status": "Approved",
                'apply_date': "2024-09-30",
                'request_reason': "Personal matters"
                })
        
        self.assertEqual(response.get_json()["decision"], {
            "decision_id": 1,
            "request_id": "2",
            'specific_date': "2024-09-15",
            "manager_id": 140001,
            "decision_date": "2024-12-12",
            "decision_status": "Approved",
            "decision_notes": "Nil"
        })

    def test_headcount_check_above_50_percent(self):
        wfh_request_1 = WFHRequests(
            request_id="1",
            staff_id=140008,
            manager_id=140001,
            specific_date=datetime.strptime("2024-09-15", '%Y-%m-%d'),
            request_status='Approved',
            apply_date=date(2024, 9, 30),
            request_reason='Personal matters',
            is_am=False,
            is_pm=True
        )
        db.session.add(wfh_request_1)

        wfh_request_2 = WFHRequests(
            request_id="2",
            staff_id=140009,
            manager_id=140001,
            specific_date=datetime.strptime("2024-09-15", '%Y-%m-%d'),
            request_status='Pending',
            apply_date=date(2024, 9, 30),
            request_reason='Personal matters',
            is_am=False,
            is_pm=True
        )
        db.session.add(wfh_request_2)

        wfh_request_3 = WFHRequests(
            request_id="3",
            staff_id=140010,
            manager_id=140001,
            specific_date=datetime.strptime("2024-09-15", '%Y-%m-%d'),
            request_status='Approved',
            apply_date=date(2024, 9, 30),
            request_reason='Personal matters',
            is_am=False,
            is_pm=True
        )
        db.session.add(wfh_request_3)
        db.session.commit()

        request_body = {
            'request_id': "2",
            'decision_status': 'Approved',
            'decision_notes': 'Nil',
            'manager_id': "140001"
        }

        response = self.client.post("/api/approve",
                                    data=json.dumps(request_body),
                                    content_type='application/json')
        
        self.assertEqual(response.status_code, 422)
        self.assertEqual(response.get_json(), {"error": "Exceed 0.5 rule limit for PM session"})

    @patch('util.request_decisions.date')
    def test_headcount_check_exactly_50_percent(self, mock_datetime):
        mock_datetime.today.return_value = date(2024, 12, 12)
        wfh_request_1 = WFHRequests(
            request_id="1",
            staff_id=140008,
            manager_id=140001,
            specific_date=datetime.strptime("2024-09-15", '%Y-%m-%d'),
            request_status='Approved',
            apply_date=date(2024, 9, 30),
            request_reason='Personal matters',
            is_am=False,
            is_pm=True
        )
        db.session.add(wfh_request_1)

        wfh_request_2 = WFHRequests(
            request_id="2",
            staff_id=140009,
            manager_id=140001,
            specific_date=datetime.strptime("2024-09-15", '%Y-%m-%d'),
            request_status='Pending',
            apply_date=date(2024, 9, 30),
            request_reason='Personal matters',
            is_am=False,
            is_pm=True
        )
        db.session.add(wfh_request_2)

        db.session.commit()

        request_body = {
            'request_id': "2",
            'decision_status': 'Approved',
            'decision_notes': 'Nil',
            'manager_id': "140001"
        }

        response = self.client.post("/api/approve",
                                    data=json.dumps(request_body),
                                    content_type='application/json')

        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.get_json()["message"], "Request updated and manager's decision stored successfully")
        self.assertEqual(response.get_json()["request"], {
                'request_id': "2",
                'staff_id': 140009,
                'manager_id': 140001,
                'specific_date': "2024-09-15",
                'is_am': False,
                'is_pm': True,
                "request_status": "Approved",
                'apply_date': "2024-09-30",
                'request_reason': "Personal matters"
                })
        
        self.assertEqual(response.get_json()["decision"], {
            "decision_id": 1,
            "request_id": "2",
            'specific_date': "2024-09-15",
            "manager_id": 140001,
            "decision_date": "2024-12-12",
            "decision_status": "Approved",
            "decision_notes": "Nil"
        })

    def test_approve_recurring_invalid_json(self):
        request_body = {}
        response = self.client.post("/api/approve_recurring",
                                     data=json.dumps(request_body),
                                     content_type='application/json')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.get_json(), {"error": "Invalid JSON or no data provided"})

    def test_approve_recurring_missing_field(self):
        request_body = {
            'manager_id': 140001,
            "decision_notes": "Nil",
            'decision_status': 'Approved'
        }
        response = self.client.post("/api/approve_recurring",
                                     data=json.dumps(request_body),
                                     content_type='application/json')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.get_json(), {"error": f"Missing 'request_id' in request"})

    def test_approve_recurring_request_not_found(self):
        request_body = {
            'request_id': 999,
            "decision_status" : 'Approved', 
            "decision_notes": 'NIL', 
            "manager_id": 140001, 
            "specific_date": '15-09-2024'
        }
        response = self.client.post("/api/approve_recurring",
                                     data=json.dumps(request_body),
                                     content_type='application/json')
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.get_json(), {"error": "Request not found"})

    def test_approve_recurring_success(self):
        req = WFHRequests(
            request_id=3,
            staff_id=140008,
            manager_id=140001,
            specific_date = date(2024, 9, 15), 
            is_am = True,
            is_pm = False,
            request_status='Pending',
            apply_date=date(2024, 9, 10), 
            request_reason = 'party'
        )
        db.session.add(req)
        db.session.commit()

        request_body = {
            'request_id': 3,
            'decision_status':'Approved', 
            'decision_notes': 'Nil', 
            'manager_id': 14001,
            'specific_date': '2024-09-15'

        }
        response = self.client.post("/api/approve_recurring",
                                    data=json.dumps(request_body),
                                    content_type='application/json')

        self.assertEqual(response.status_code, 201)
        self.assertIn("Recurring WFH requests processed successfully", response.get_json()["message"])

    def test_approve_recurring_headcount_exceed(self):
        wfh_request_1 = WFHRequests(
            request_id=1,
            staff_id=140008,
            manager_id=140001,
            specific_date = date(2024, 9, 16), 
            is_am=False, 
            is_pm=True,
            request_status='Approved',
            apply_date=datetime.now(),
            request_reason='Personal matters',
        )
        db.session.add(wfh_request_1)

        wfh_request_2 = WFHRequests(
            request_id=3,
            staff_id=140010,
            manager_id=140001,
            specific_date = date(2024, 9, 16),
            request_status='Approved',
            apply_date=datetime.now(),
            request_reason='Personal matters',
            is_am=False,
            is_pm=True
        )
        db.session.add(wfh_request_2)

        wfh_request_3 = WFHRequests(
            request_id=2,
            staff_id=140009,
            manager_id=140001,
            specific_date = date(2024, 9, 16),
            request_status='Pending',
            apply_date=datetime.now(),
            request_reason='Personal matters',
            is_am=False,
            is_pm=True
        )
        db.session.add(wfh_request_3)
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

    def test_manager_approve_withdrawal_success_approve(self):
        wfh_request_1 = WFHRequests(
            request_id=1,
            staff_id=140008,
            manager_id=140001,
            specific_date=datetime.strptime("2024-09-15", '%Y-%m-%d'),
            request_status='Pending_Withdraw',
            apply_date=date(2024, 9, 30),
            request_reason='Personal matters',
            is_am=False,
            is_pm=True
        )
        db.session.add(wfh_request_1)
        db.session.commit()

        request_body = {
            "request_id": 1,
            "specific_date": "2024-09-15",
            "manager_id": 140001,
            "decision_status": "Approved",
            "decision_notes": "Approved by manager"
        }
        response = self.client.post('/api/approve_withdrawal', 
                                    data=json.dumps(request_body), 
                                    content_type='application/json')
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.get_json()['message'], "Withdrawal request updated and manager's decision stored successfully")
        self.assertEqual(response.get_json()["request"],{
            "request_id": "1",
            "specific_date": "2024-09-15",
            "staff_id": 140008,
            "manager_id": 140001,
            "is_am": False,
            "is_pm": True,
            "request_status": "Withdrawn",
            "apply_date": "2024-09-30",
            "request_reason": "Personal matters"
        })
        self.assertEqual(response.get_json()["decision"], {
            "withdraw_decision_id": 1,
            "request_id": "1",
            "specific_date": "2024-09-15",
            "manager_id": 140001,
            "decision_date": str(datetime.now().date()),
            "decision_status": "Approved",
            "decision_notes": "Approved by manager"
        })

    def test_manager_approve_withdrawal_success_reject(self):
        wfh_request_1 = WFHRequests(
            request_id=1,
            staff_id=140008,
            manager_id=140001,
            specific_date=datetime.strptime("2024-09-15", '%Y-%m-%d'),
            request_status='Pending_Withdraw',
            apply_date=date(2024, 9, 30),
            request_reason='Personal matters',
            is_am=False,
            is_pm=True
        )
        db.session.add(wfh_request_1)
        db.session.commit()

        request_body = {
            "request_id": 1,
            "specific_date": "2024-09-15",
            "manager_id": 140001,
            "decision_status": "Rejected",
            "decision_notes": "Rejected by manager"
        }
        response = self.client.post('/api/approve_withdrawal', 
                                    data=json.dumps(request_body), 
                                    content_type='application/json')
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.get_json()['message'], "Withdrawal request updated and manager's decision stored successfully")
        self.assertEqual(response.get_json()["request"],{
            "request_id": "1",
            "specific_date": "2024-09-15",
            "staff_id": 140008,
            "manager_id": 140001,
            "is_am": False,
            "is_pm": True,
            "request_status": "Approved",
            "apply_date": "2024-09-30",
            "request_reason": "Personal matters"
        })
        self.assertEqual(response.get_json()["decision"], {
            "withdraw_decision_id": 1,
            "request_id": "1",
            "specific_date": "2024-09-15",
            "manager_id": 140001,
            "decision_date": str(datetime.now().date()),
            "decision_status": "Rejected",
            "decision_notes": "Rejected by manager"
        })



    def test_manager_approve_withdrawal_invalid_json(self):
        request_body = {}
        response = self.client.post('/api/approve_withdrawal', 
                                    data=json.dumps(request_body), 
                                    content_type='application/json')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.get_json(), {"error": "Invalid JSON or no data provided"})

    def test_manager_approve_withdrawal_missing_field(self):
        request_body = {
            'manager_id': 140001,
            "decision_notes": "Nil",
            'decision_status': 'Approved'
        }
        response = self.client.post("/api/approve_withdrawal",
                                     data=json.dumps(request_body),
                                     content_type='application/json')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.get_json(), {"error": f"Missing 'request_id' in request"})
    
    def test_manager_approve_withdrawal_missing_employee(self):
        wfh_request_1 = WFHRequests(
            request_id=1,
            staff_id=140099,
            manager_id=140001,
            specific_date=datetime.strptime("2024-09-15", '%Y-%m-%d'),
            request_status='Pending_Withdraw',
            apply_date=date(2024, 9, 30),
            request_reason='Personal matters',
            is_am=False,
            is_pm=True
        )
        db.session.add(wfh_request_1)
        db.session.commit()
        request_body = {
            'request_id': 1,
            'specific_date': "2024-09-15",
            'manager_id': 140001,
            "decision_notes": "Nil",
            'decision_status': 'Approved'
        }
        response = self.client.post("/api/approve_withdrawal",
                                     data=json.dumps(request_body),
                                     content_type='application/json')
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.get_json(), {"error": f"Employee with staff_id {wfh_request_1.staff_id} not found"})

    def test_manager_approve_withdrawal_request_not_found(self):
        request_body = {
            "request_id": 999,
            "specific_date": "2024-09-15",
            "manager_id": 140001,
            "decision_status": "Approved",
            "decision_notes": "Approved by manager"
        }
        response = self.client.post('/api/approve_withdrawal', 
                                    data=json.dumps(request_body), 
                                    content_type='application/json')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.get_json(), {"error": "Request not found"})

    def test_manager_approve_withdrawal_manager_id_not_found(self):
        wfh_request_1 = WFHRequests(
            request_id=1,
            staff_id=140008,
            manager_id=140001,
            specific_date=datetime.strptime("2024-09-15", '%Y-%m-%d'),
            request_status='Pending_Withdraw',
            apply_date=date(2024, 9, 30),
            request_reason='Personal matters',
            is_am=False,
            is_pm=True
        )
        db.session.add(wfh_request_1)
        db.session.commit()
        request_body = {
            "request_id": 1,  
            "specific_date": "2024-09-15",
            "manager_id": 999999,  # Using an invalid/non-existent manager ID
            "decision_status": "Approved",
            "decision_notes": "Approved by manager"
        }
        response = self.client.post('/api/approve_withdrawal', 
                                    data=json.dumps(request_body), 
                                    content_type='application/json')
        
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.get_json(), {"error": f"Reporting manager not found"})

    def test_manager_approve_withdrawal_wrong_manager_id(self):
        wfh_request_1 = WFHRequests(
            request_id=1,
            staff_id=140008,
            manager_id=140001,
            specific_date=datetime.strptime("2024-09-15", '%Y-%m-%d'),
            request_status='Pending_Withdraw',
            apply_date=date(2024, 9, 30),
            request_reason='Personal matters',
            is_am=False,
            is_pm=True
        )
        db.session.add(wfh_request_1)
        db.session.commit()
        request_body = {
            "request_id": 1,  
            "specific_date": "2024-09-15",
            "manager_id": 140002,  # Using wrong manager ID
            "decision_status": "Approved",
            "decision_notes": "Approved by manager"
        }
        response = self.client.post('/api/approve_withdrawal', 
                                    data=json.dumps(request_body), 
                                    content_type='application/json')
        
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.get_json(), {"error": f"Employee {wfh_request_1.staff_id} reports under {wfh_request_1.manager_id} instead of {request_body['manager_id']}"})

    def test_manager_approve_withdrawal_wrong_status(self):
        wfh_request_1 = WFHRequests(
            request_id=1,
            staff_id=140008,
            manager_id=140001,
            specific_date=datetime.strptime("2024-09-15", '%Y-%m-%d'),
            request_status='Approved',
            apply_date=date(2024, 9, 30),
            request_reason='Personal matters',
            is_am=False,
            is_pm=True
        )
        db.session.add(wfh_request_1)
        db.session.commit()
        request_body = {
            "request_id": 1,  
            "specific_date": "2024-09-15",
            "manager_id": 140001, 
            "decision_status": "Approved",
            "decision_notes": "Approved by manager"
        }
        response = self.client.post('/api/approve_withdrawal', 
                                    data=json.dumps(request_body), 
                                    content_type='application/json')
        
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.get_json(), {"error": f"Manager cannot approve or reject request with {wfh_request_1.request_status} status"})

    def test_manager_approve_withdrawal_invalid_decision_status(self):
        wfh_request_1 = WFHRequests(
            request_id=1,
            staff_id=140008,
            manager_id=140001,
            specific_date=datetime.strptime("2024-09-15", '%Y-%m-%d'),
            request_status='Pending_Withdraw',
            apply_date=date(2024, 9, 30),
            request_reason='Personal matters',
            is_am=False,
            is_pm=True
        )
        db.session.add(wfh_request_1)
        db.session.commit()
        request_body = {
            "request_id": 1,  
            "specific_date": "2024-09-15",
            "manager_id": 140001, 
            "decision_status": "",
            "decision_notes": "Approved by manager"
        }
        response = self.client.post('/api/approve_withdrawal', 
                                    data=json.dumps(request_body), 
                                    content_type='application/json')
        
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.get_json(), {"error": f"Invalid decision status"})



if __name__ == "__main__":
    unittest.main()
