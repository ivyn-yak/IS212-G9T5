import unittest
from server import app, db
from models import *
import datetime

# class TestEmployee(unittest.TestCase):
#     def test_json(self):
#         e = Employee(name='Phris Coskitt', title='HRH')
#         self.assertEqual(e.json(), {
#             'id': None,
#             'name': 'Phris Coskitt',
#             'title': 'HRH'}
#         )

class TestWFHRequests(unittest.TestCase):
    def test_json(self):
        req = WFHRequests(
            staff_id=140008,
            manager_id=140001,
            request_type="Ad-hoc",  
            start_date=datetime.date(2024, 9, 15),  
            end_date=datetime.date(2024, 9, 15),
            recurrence_days="",
            is_am=True,
            is_pm=True, 
            request_status= "Pending",  
            apply_date=datetime.date(2024, 9, 30),
            withdrawable_until=datetime.date(2024, 10, 14),
            request_reason="Sick"
            )

        self.assertEqual(req.json(), {
            'request_id': None,
            'staff_id': 140008,
            'manager_id': 140001,
            'request_type': 'Ad-hoc',
            'start_date': "2024-09-15",
            'end_date': "2024-09-15",
            'recurrence_days': '',
            'is_am': True,
            'is_pm': True,
            "request_status": "Pending",
            'apply_date': "2024-09-30",
            'withdrawable_until': "2024-10-14",
            'request_reason': "Sick"
        })

# class TestWFHRequestDates(unittest.TestCase):
#     def test_to_dict(self):
#         p1 = WFHRequestDates(name='Kankan', title='Lord',
#                      contact_num='+65 8888 8888', ewallet_balance=88)
#         self.assertEqual(p1.to_dict(), {
#             'id': None,
#             'name': 'Kankan',
#             'title': 'Lord',
#             'contact_num': '+65 8888 8888',
#             'ewallet_balance': 88}
#         )

# class TestRequestDecisions(unittest.TestCase):
#     def test_to_dict(self):
#         c1 = RequestDecisions(diagnosis='Nosebleed',
#                           prescription='Tissue paper for nose',
#                           charge=55, doctor_id=8, patient_id=9)
#         self.assertEqual(c1.to_dict(), {
#             'id': None,
#             'diagnosis': 'Nosebleed',
#             'prescription': 'Tissue paper for nose',
#             'charge': 55,
#             'doctor_id': 8,
#             'patient_id': 9
#             }
#         )


if __name__ == "__main__":
    unittest.main()
