import unittest
import flask_testing
from server import app, db
from models import Employee

class TestApp(flask_testing.TestCase):
    app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite://"
    app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {}
    app.config['TESTING'] = True

    def create_app(self):
        return app

    def setUp(self):
        db.create_all()
        manager = Employee(
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

        employee = Employee(
            staff_id=140880,
            staff_fname="Heng",
            staff_lname="Chan",
            dept="Sales",
            position="Account Manager",
            country="Singapore",
            email="Heng.Chan@allinone.com.sg",
            reporting_manager=140008,
            role=2
        )

        db.session.add(manager)
        db.session.add(employee)
        db.session.commit()
        
    def tearDown(self):
        db.session.remove()
        db.drop_all()

class TestEmployee(TestApp):
    def test_get_employee(self):
        staff_id = 140008

        response = self.client.get(f"/api/{staff_id}",
                                    content_type='application/json')
        
        self.assertEqual(response.get_json(), {
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

    def test_get_employee_invalid(self):
        staff_id = 0

        response = self.client.get(f"/api/{staff_id}",
                                    content_type='application/json')
        
        self.assertEqual(response.get_json(), {"error": f"Staff 0 not found"})

    def test_get_employee_role(self):
        staff_id = 140008

        response = self.client.get(f"/api/role/{staff_id}",
                                    content_type='application/json')
        
        self.assertEqual(response.get_json(), {"staff_id": 140008, "role": 3 })

    def test_get_employee_role_invalid(self):
        staff_id = 0

        response = self.client.get(f"/api/role/{staff_id}",
                                    content_type='application/json')
        
        self.assertEqual(response.get_json(), {"error": f"Staff 0 not found"})
    
    def test_get_team_invalid(self):
        staff_id = 0

        response = self.client.get(f"/api/team/{staff_id}",
                                    content_type='application/json')
        
        self.assertEqual(response.get_json(), {"error": f"Staff 0 not found"})

    def test_get_team_staff(self):
        staff_id = 140880

        response = self.client.get(f"/api/team/{staff_id}",
                                    content_type='application/json')
        
        self.assertEqual(response.get_json(), [
            {
                "country": "Singapore",
                "dept": "Sales",
                "email": "Heng.Chan@allinone.com.sg",
                "position": "Account Manager",
                "reporting_manager": 140008,
                "role": 2,
                "staff_fname": "Heng",
                "staff_id": 140880,
                "staff_lname": "Chan"
            }
        ])

    def test_get_team_manager(self):
        staff_id = 140008

        response = self.client.get(f"/api/team/{staff_id}",
                                    content_type='application/json')
        
        self.assertEqual(response.get_json(), [
            {
                "country": "Singapore",
                "dept": "Sales",
                "email": "Heng.Chan@allinone.com.sg",
                "position": "Account Manager",
                "reporting_manager": 140008,
                "role": 2,
                "staff_fname": "Heng",
                "staff_id": 140880,
                "staff_lname": "Chan"
            }
        ])

if __name__ == '__main__':
    unittest.main()
