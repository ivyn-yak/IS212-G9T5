from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import *

db = SQLAlchemy()

class Employee(db.Model):
    __tablename__ = 'employee'

    staff_id = Column(Integer, primary_key=True)
    staff_fname = Column(String, nullable=False)
    staff_lname = Column(String, nullable=False)
    dept = Column(String, nullable=False)
    position = Column(String, nullable=False)
    country = Column(String, nullable=False)
    email = Column(String, nullable=False)
    reporting_manager = Column(Integer, ForeignKey('employee.staff_id'))
    role = Column(Integer, nullable=False)

    def json(self):
        return {
            "staff_id": self.staff_id,
            "staff_fname": self.staff_fname,
            "staff_lname": self.staff_lname,
            "dept": self.dept,
            "position": self.position,
            "country": self.country,
            "email": self.email,
            "reporting_manager": self.reporting_manager,
            "role": self.role
        }