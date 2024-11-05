// src/components/WithdrawalForm.jsx
import React, { useState, useEffect } from 'react';
import { format } from 'date-fns';
import { fetchApprovedSchedules, submitWithdrawal } from '../../api/withdrawFormApi';
import './WithdrawalForm.css';

const WithdrawalForm = ({ staffId }) => {
  const [approvedSchedules, setApprovedSchedules] = useState([]);
  const [selectedSchedule, setSelectedSchedule] = useState('');
  const [reason, setReason] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [message, setMessage] = useState('');

  const loadApprovedSchedules = async () => {
    const { data, error } = await fetchApprovedSchedules(staffId);
    setApprovedSchedules(data);
    if (error) {
      setMessage(error);
    } else {
      setMessage('');
    }
  };

  useEffect(() => {
    loadApprovedSchedules();
  }, [staffId]);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setIsLoading(true);
    
    try {
      const selectedRequest = approvedSchedules.find(
        schedule => schedule.id === selectedSchedule
      );

      if (!selectedRequest) {
        setMessage('Invalid schedule selected');
        return;
      }

      const { success, error } = await submitWithdrawal({
        request_id: selectedSchedule,
        reason: reason,
        specific_date: selectedRequest.specific_date
      });

      if (!success) {
        setMessage(error);
        return;
      }

      setMessage('Withdrawal submitted successfully');
      setSelectedSchedule('');
      setReason('');
      loadApprovedSchedules();
    } catch (error) {
      setMessage('Failed to submit withdrawal');
    } finally {
      setIsLoading(false);
    }
  };

  if (message === 'You have no approved requests to withdraw') {
    return <div className="withdrawal-form">{message}</div>;
  }

  return (
    <form className="withdrawal-form" onSubmit={handleSubmit}>
      {message && <div className="message">{message}</div>}
      <div className="form-group">
        <label htmlFor="schedule">Select schedule you wish to withdraw</label>
        <select
          id="schedule"
          value={selectedSchedule}
          onChange={(e) => setSelectedSchedule(e.target.value)}
          required
        >
          <option value="">Select a schedule</option>
          {approvedSchedules.map((schedule) => (
            <option key={schedule.id} value={schedule.id}>
              {format(new Date(schedule.specific_date), 'yyyy-MM-dd')} : {schedule.type}
            </option>
          ))}
        </select>
      </div>
      <div className="form-group">
        <label htmlFor="reason">Please state reason for Withdrawal</label>
        <textarea
          id="reason"
          value={reason}
          onChange={(e) => setReason(e.target.value)}
          required
        />
      </div>
      <button 
        type="submit" 
        className="submit-btn"
        disabled={isLoading}
      >
        {isLoading ? "Submitting..." : "Submit"}
      </button>
    </form>
  );
};

export default WithdrawalForm;