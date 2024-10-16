import unittest
import flask_testing
from server import app, db
from models import *
import datetime

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

        wfh_request1 = WFHRequests(
                staff_id=140008,
                manager_id=140001,
                request_type='Ad-hoc',
                start_date=datetime.date(2024, 9, 15),
                end_date=datetime.date(2024, 9, 15),
                recurrence_days= None,
                is_am=True,
                is_pm=True,
                request_status='Approved',
                apply_date=datetime.date(2024, 9, 30),
                withdrawable_until=datetime.date(2024, 9, 29),
                request_reason="Sick"
            )
        
        wfh_request2 = WFHRequests(
                staff_id=140008,
                manager_id=140001,
                request_type='Ad-hoc',
                start_date=datetime.date(2024, 10, 1),
                end_date=datetime.date(2024, 10, 1),
                recurrence_days= None,
                is_am=True,
                is_pm=True,
                request_status='Pending',
                apply_date=datetime.date(2024, 9, 30),
                withdrawable_until=datetime.date(2024, 10, 15),
                request_reason="Sick"
            )

        db.session.add(employee)
        db.session.add(manager)
        db.session.add(wfh_request1)
        db.session.add(wfh_request2)
        db.session.commit()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

class TestStaffRequests(TestApp):
    def test_staff_requests(self):
        response = self.client.get("/api/140008", content_type='application/json')
        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_json()["data"], [{
                'request_id': 1,
                'staff_id': 140008,
                'manager_id': 140001,
                'request_type': 'Ad-hoc',
                'start_date': "2024-09-15",
                'end_date': "2024-09-15",
                'recurrence_days': None,
                'is_am': True,
                'is_pm': True,
                "request_status": "Approved",
                'apply_date': "2024-09-30",
                'withdrawable_until': "2024-09-29",
                'request_reason': "Sick"
                }, {
                'request_id': 2,
                'staff_id': 140008,
                'manager_id': 140001,
                'request_type': 'Ad-hoc',
                'start_date': "2024-10-01",
                'end_date': "2024-10-01",
                'recurrence_days': None,
                'is_am': True,
                'is_pm': True,
                "request_status": "Pending",
                'apply_date': "2024-09-30",
                'withdrawable_until': "2024-10-15",
                'request_reason': "Sick"
                }]
            )
        
    def test_staff_no_requests(self):
        response = self.client.get("/api/140001", content_type='application/json')
        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_json()["data"], [])

    def test_invalid_staff(self):
        response = self.client.get("/api/0", content_type='application/json')
        
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.get_json(), {"error": "Staff not found"})

    def test_staff_pending(self):
        response = self.client.get("/api/140008/pending", content_type='application/json')
        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_json()["data"], [{
                'request_id': 2,
                'staff_id': 140008,
                'manager_id': 140001,
                'request_type': 'Ad-hoc',
                'start_date': "2024-10-01",
                'end_date': "2024-10-01",
                'recurrence_days': None,
                'is_am': True,
                'is_pm': True,
                "request_status": "Pending",
                'apply_date': "2024-09-30",
                'withdrawable_until': "2024-10-15",
                'request_reason': "Sick"
                }]
            )
    
    def test_staff_no_pending(self):
        response = self.client.get("/api/140001/pending", content_type='application/json')
        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_json()["data"], [])

    def test_invalid_staff_pending(self):
        response = self.client.get("/api/0/pending", content_type='application/json')
        
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.get_json(), {"error": "Staff not found"})

class TestCancelRequest(TestApp):
    
    def test_cancel_pending_request_success(self):
        # Ensure the request is pending and within the allowed date range
        wfh_request = WFHRequests.query.filter_by(request_id=2).first()
        wfh_request.start_date = datetime.date(2024, 10, 1)  # Within valid range
        wfh_request.request_status = 'Pending'
        db.session.commit()

        response = self.client.put(
            "/api/staff/140008/cancel_request/2",
            json={"cancellation_reason": "Changed my mind"},
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_json(), {"message": "Request cancelled successfully"})

        # Verify request status in the database
        wfh_request = WFHRequests.query.filter_by(request_id=2).first()
        self.assertEqual(wfh_request.request_status, 'Cancelled')
        self.assertEqual(wfh_request.request_reason, 'Changed my mind')


    def test_cancel_approved_request(self):
        # Test cancelling an already approved request
        response = self.client.put(
            "/api/staff/140008/cancel_request/1",
            json={"cancellation_reason": "Change of plans"},
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.get_json(), {"error": "Only pending requests can be cancelled"})

    def test_cancel_request_without_reason(self):
        response = self.client.put(
            "/api/staff/140008/cancel_request/2",
            json={},  # No cancellation reason provided
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.get_json(), {"error": "Cancellation reason is required"})


    def test_cancel_nonexistent_request(self):
        # Test cancelling a non-existent request
        response = self.client.put(
            "/api/staff/140008/cancel_request/999",  # Request ID 999 doesn't exist
            json={"cancellation_reason": "Not needed"},
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.get_json(), {"error": "Request not found or not owned by this staff member"})

    def test_cancel_request_outside_allowed_date_range(self):
        # Set the request status to pending and update the start_date
        wfh_request = WFHRequests.query.filter_by(request_id=2).first()
        wfh_request.start_date = datetime.date(2025, 2, 1)  # Set date too far in advance
        wfh_request.request_status = 'Pending'
        db.session.commit()

        response = self.client.put(
            "/api/staff/140008/cancel_request/2",
            json={"cancellation_reason": "Change of plans"},
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.get_json(), {"error": "Requests can only be cancelled 3 months in advance and 1 month back"})



if __name__ == '__main__':
    unittest.main()


