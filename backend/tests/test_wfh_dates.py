import unittest
import flask_testing
from server import app, db
from models import Employee, WFHRequests, WFHRequestDates
from datetime import date

class TestApp(flask_testing.TestCase):
    app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite://"
    app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {}
    app.config['TESTING'] = True

    def create_app(self):
        return app

    def setUp(self):
        db.create_all()

        # Create Employee records based on employeenew.pdf data
        employee1 = Employee(
            staff_id=140002,
            staff_fname="Susan",
            staff_lname="Goh",
            dept="Sales",
            position="Account Manager",
            country="Singapore",
            email="Susan.Goh@allinone.com.sg",
            reporting_manager=140894,
            role=2
        )
        manager = Employee(
            staff_id=140894,
            staff_fname="Rahim",
            staff_lname="Khalid",
            dept="Sales",
            position="Sales Manager",
            country="Singapore",
            email="Rahim.Khalid@allinone.com.sg",
            reporting_manager=140001,
            role=3
        )
        db.session.add(employee1)
        db.session.add(manager)

        # Create WFHRequests record
        wfh_request = WFHRequests(
            staff_id=140002,
            manager_id=140894,
            request_type='Ad-hoc',
            start_date=date(2024, 9, 24),
            end_date=date(2024, 9, 24),
            is_am=True,
            is_pm=False,
            request_status='Pending',
            apply_date=date(2024, 9, 20),
            withdrawable_until=date(2024, 9, 23),
            request_reason="Personal"
        )
        db.session.add(wfh_request)
        db.session.flush()  # Flush to get the request_id for the next record

        # Create WFHRequestDates record
        wfh_request_date = WFHRequestDates(
            request_id=wfh_request.request_id,
            staff_id=140002,
            specific_date=date(2024, 9, 24),
            is_am=True,
            is_pm=False
        )
        db.session.add(wfh_request_date)

        db.session.commit()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

class TestWFHDates(TestApp):

    def test_get_staff_wfh_dates(self):
        staff_id = 140002
        response = self.client.get(f"/api/staff/{staff_id}/wfh_dates", content_type='application/json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, [{
            "date_id": 1,
            "request_id": 1,
            "staff_id": 140002,
            "specific_date": "2024-09-24",
            "is_am": True,
            "is_pm": False
        }])

    def test_get_staff_wfh_dates_in_range(self):
        staff_id = 140002
        response = self.client.get(f"/api/staff/{staff_id}/wfh_dates?start_date=2024-09-01&end_date=2024-09-30", content_type='application/json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, [{
            "date_id": 1,
            "request_id": 1,
            "staff_id": 140002,
            "specific_date": "2024-09-24",
            "is_am": True,
            "is_pm": False
        }])

    def test_get_staff_wfh_and_office_dates_in_range(self):
        staff_id = 140002
        response = self.client.get(f"/api/staff/{staff_id}/wfh_office_dates?start_date=2024-09-01&end_date=2024-09-30", content_type='application/json')
        self.assertEqual(response.status_code, 200)
        expected_response = {
            "wfh_dates": [{
                "date_id": 1,
                "request_id": 1,
                "staff_id": 140002,
                "specific_date": "2024-09-24",
                "is_am": True,
                "is_pm": False
            }],
            "in_office_dates": [
                {"date": "2024-09-01", "is_am": True, "is_pm": True},
                # Other in-office dates within the range
                {"date": "2024-09-24", "is_am": False, "is_pm": True},  # Not WFH for PM
                # ...
                {"date": "2024-09-30", "is_am": True, "is_pm": True}
            ]
        }
        self.assertEqual(response.json["wfh_dates"], expected_response["wfh_dates"])

    def test_get_team_wfh_schedule(self):
        staff_id = 140002
        response = self.client.get(f"/api/staff/{staff_id}/team_wfh_schedule?start_week_date=2024-09-20", content_type='application/json')
        self.assertEqual(response.status_code, 200)
        expected_response = {
            "staff": {
                "staff_id": 140002,
                "ScheduleDetails": [{
                    "date_id": 1,
                    "request_id": 1,
                    "staff_id": 140002,
                    "specific_date": "2024-09-24",
                    "is_am": True,
                    "is_pm": False
                }]
            },
            "team": [
                # Any other team members (if applicable)
            ]
        }
        self.assertEqual(response.json["staff"], expected_response["staff"])

    def test_get_department_schedules(self):
        response = self.client.get(f"/api/departments/schedules?start_week_date=2024-09-20", content_type='application/json')
        self.assertEqual(response.status_code, 200)
        expected_response = [
            {
                "department_name": "Sales",
                "teams": [
                    [
                        {
                            "staff_id": 140002,
                            "ScheduleDetails": [{
                                "date_id": 1,
                                "request_id": 1,
                                "staff_id": 140002,
                                "specific_date": "2024-09-24",
                                "is_am": True,
                                "is_pm": False
                            }]
                        },
                        # Any other members in the team
                    ]
                ]
            }
            # Any other departments
        ]
        self.assertEqual(response.json[0]["department_name"], expected_response[0]["department_name"])

if __name__ == '__main__':
    unittest.main()
