from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import *

db = SQLAlchemy()

#Employee Table
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
    
# WFHRequests Table
class WFHRequests(db.Model):
    __tablename__ = 'work_from_home_requests'

    request_id = Column(Integer, primary_key=True)
    staff_id = Column(Integer, ForeignKey('employee.staff_id'), nullable=False)
    request_type = Column(Enum('Ad-hoc', 'Recurring', name='request_type'), nullable=False)
    start_date = Column(Date, nullable=False)
    end_date = Column(Date, nullable=False)
    recurrence_days = Column(String, nullable=True)  #  "Mon,Wed"
    request_status = Column(Enum('Pending', 'Approved', 'Rejected', name='request_status'), nullable=False)
    apply_date = Column(Date, nullable=False)
    withdrawable_until = Column(Date, nullable=False)
    request_reason = Column(String, nullable=True)

    employee = db.relationship('Employee')

    def json(self):
        return {
            "request_id": self.request_id,
            "staff_id": self.staff_id,
            "request_type": self.request_type,
            "start_date": str(self.start_date),
            "end_date": str(self.end_date),
            "recurrence_days": self.recurrence_days,
            "request_status": self.request_status,
            "apply_date": str(self.apply_date),
            "withdrawable_until": str(self.withdrawable_until),
            "request_reason": self.request_reason
        }

# WFHRequestDates Table
class WFHRequestDates(db.Model):
    __tablename__ = 'work_from_home_request_dates'

    date_id = Column(Integer, primary_key=True)
    request_id = Column(Integer, ForeignKey('work_from_home_requests.request_id'), nullable=False)
    specific_date = Column(Date, nullable=False)

    work_from_home_request = db.relationship('WFHRequests')

    def json(self):
        return {
            "date_id": self.date_id,
            "request_id": self.request_id,
            "specific_date": str(self.specific_date)
        }
