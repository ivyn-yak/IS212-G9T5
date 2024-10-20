from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import *
from sqlalchemy.dialects.postgresql import UUID
import uuid

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
    __tablename__ = 'wfhrequests'

    request_id = Column(String, nullable=False)
    staff_id = Column(Integer, ForeignKey('employee.staff_id'), nullable=False)
    manager_id = Column(Integer, ForeignKey('employee.staff_id'), nullable=False)  
    specific_date = Column(Date, nullable=False)    
    is_am = Column(Boolean, nullable=False, default=False)  # Is AM selected?
    is_pm = Column(Boolean, nullable=False, default=False)  # Is PM selected?
    request_status = Column(Enum('Pending', 'Approved', 'Rejected', 'Cancelled', 'Withdrawn', 'Pending_Withdraw', name='request_status'), nullable=False)
    apply_date = Column(Date, nullable=False)
    request_reason = Column(Text, nullable=True)

    employee = db.relationship('Employee', foreign_keys=[staff_id])
    
    __table_args__ = (
        PrimaryKeyConstraint('request_id', 'specific_date'),
    )

    def json(self):
        return {
            "request_id": str(self.request_id),
            "staff_id": self.staff_id,
            "manager_id": self.manager_id,
            "specific_date": str(self.specific_date),
            "is_am": self.is_am,
            "is_pm": self.is_pm,
            "request_status": self.request_status,
            "apply_date": str(self.apply_date),
            "request_reason": self.request_reason
        }

# RequestDecisions Table (Stores the decision made by the manager for the requests)
class RequestDecisions(db.Model):
    __tablename__ = 'requestdecisions'

    decision_id = Column(Integer, primary_key=True)
    request_id = Column(String, ForeignKey('wfhrequests.request_id'), nullable=False)
    manager_id = Column(Integer, ForeignKey('employee.staff_id'), nullable=False)  # Manager who made the decision
    decision_date = Column(Date, nullable=False)
    decision_status = Column(Enum('Approved', 'Rejected', name='decision_status'), nullable=False)
    decision_notes = Column(Text, nullable=True)

    manager = db.relationship('Employee', foreign_keys=[manager_id])
    work_from_home_request = db.relationship('WFHRequests')

    def json(self):
        return {
            "decision_id": self.decision_id,
            "request_id": str(self.request_id),
            "manager_id": self.manager_id,
            "decision_date": str(self.decision_date),
            "decision_status": self.decision_status,
            "decision_notes": self.decision_notes
        }
    
# WithdrawDecisions Table (Stores the decision made by the manager for the withdraw requests)
class WithdrawDecisions(db.Model):
    __tablename__ = 'withdrawdecisions'

    withdraw_decision_id = Column(Integer, primary_key=True)
    specific_date = Column(Date, nullable=False)
    request_id = Column(String, nullable=False)
    manager_id = Column(Integer, ForeignKey('employee.staff_id'), nullable=False)  # Manager who made the decision
    decision_date = Column(Date, nullable=False)
    decision_status = Column(Enum('Approved', 'Rejected', name='decision_status'), nullable=False)
    decision_notes = Column(Text, nullable=True)

    manager = db.relationship('Employee', foreign_keys=[manager_id])
    work_from_home_request = db.relationship(
        'WFHRequests', 
        foreign_keys=[request_id, specific_date], 
        primaryjoin='and_(WithdrawDecisions.request_id == WFHRequests.request_id, WithdrawDecisions.specific_date == WFHRequests.specific_date)'
    )

    def json(self):
        return {
            "withdraw_decision_id": self.withdraw_decision_id,
            "specific_date": str(self.specific_date),
            "request_id": str(self.request_id),
            "manager_id": self.manager_id,
            "decision_date": str(self.decision_date),
            "decision_status": self.decision_status,
            "decision_notes": self.decision_notes
        }
    
# WFHRequestLogs Table (Stores the changes made to WFHRequest)
class WFHRequestLogs(db.Model):
    __tablename__ = 'wfhrequestlogs'

    log_datetime = Column(DateTime, nullable=False)
    request_id = Column(String, ForeignKey('wfhrequests.request_id'), nullable=False)
    specific_date = Column(Date, ForeignKey('wfhrequests.specific_date'), nullable=False)  # The specific work-from-home date
    request_status = Column(Enum('Pending', 'Approved', 'Rejected', 'Cancelled', 'Withdrawn', 'Pending_Withdraw', name='request_status'), nullable=False)
    apply_log_date = Column(Date, nullable=False) # Updates when is Pending or Pending_Withdraw
    reason_log = Column(Text, nullable=True)

    work_from_home_request = db.relationship(
        'WFHRequests', 
        foreign_keys=[request_id, specific_date],
        primaryjoin='and_(WFHRequestLogs.request_id == WFHRequests.request_id, WFHRequestLogs.specific_date == WFHRequests.specific_date)'
    )

    __table_args__ = (
        PrimaryKeyConstraint('log_datetime', 'request_id', 'specific_date'),
    )

    def json(self):
        return {
            "log_datetime": str(self.log_datetime),
            "request_id": str(self.request_id),
            "specific_date": str(self.specific_date),
            "request_status": self.request_status,
            "apply_log_date": str(self.apply_log_date),
            "reason_log": self.reason_log
        }
    
