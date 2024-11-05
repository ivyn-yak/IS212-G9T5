import unittest
from flask_testing import TestCase
from server import app, db
from models import WFHRequests, WFHRequestLogs
from datetime import datetime, timedelta, timezone

class TestStaffCancelRequest(TestCase):
    app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite://"
    app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {}
    app.config['TESTING'] = True

    def create_app(self):
        return app

    def setUp(self):
        db.create_all()
        # Adding a pending WFH request for testing
        self.specific_date = (datetime.now(timezone.utc).date()).strftime('%Y-%m-%d')
        self.wfh_request = WFHRequests(
            request_id="1",
            staff_id=101,
            manager_id=201,
            specific_date=datetime.strptime(self.specific_date, '%Y-%m-%d').date(),
            is_am=True,
            is_pm=False,
            request_status='Pending',
            apply_date=datetime.now(timezone.utc).date(),
            request_reason="Medical Appointment"
        )
        db.session.add(self.wfh_request)
        db.session.commit()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def test_successful_cancellation(self):
        # Ensure the request is in the database
        response = self.client.put(
            f"/api/staff/{self.wfh_request.staff_id}/cancel_request/{self.wfh_request.request_id}/{self.specific_date}"
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json["message"], "Request cancelled successfully")

        # Check if the request status is updated
        updated_request = WFHRequests.query.filter_by(request_id=self.wfh_request.request_id, specific_date=self.wfh_request.specific_date).first()
        self.assertEqual(updated_request.request_status, "Cancelled")

        # Check if the log entry was created
        log_entry = WFHRequestLogs.query.filter_by(request_id=self.wfh_request.request_id, specific_date=self.wfh_request.specific_date).first()
        self.assertIsNotNone(log_entry)
        self.assertEqual(log_entry.request_status_log, "Cancelled")
        self.assertEqual(log_entry.reason_log, "Staff initiated cancellation")

    def test_request_not_found(self):
        response = self.client.put(
            f"/api/staff/{self.wfh_request.staff_id}/cancel_request/999/{self.specific_date}"
        )
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.json["error"], "Request not found")

    def test_non_pending_status(self):
        # Update the request to a non-pending status
        self.wfh_request.request_status = "Approved"
        db.session.commit()

        response = self.client.put(
            f"/api/staff/{self.wfh_request.staff_id}/cancel_request/{self.wfh_request.request_id}/{self.specific_date}"
        )
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json["error"], "Only pending requests can be cancelled")

    def test_invalid_date_format(self):
        # Attempt to cancel with an invalid date format
        invalid_date = "2024-13-40"  # Invalid date
        response = self.client.put(
            f"/api/staff/{self.wfh_request.staff_id}/cancel_request/{self.wfh_request.request_id}/{invalid_date}"
        )
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json["error"], "Invalid date format, please use YYYY-MM-DD")


if __name__ == '__main__':
    unittest.main()
