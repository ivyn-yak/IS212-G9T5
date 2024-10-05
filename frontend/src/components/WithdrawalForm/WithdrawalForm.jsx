import React, { useState } from 'react';
import './WithdrawalForm.css';

const WithdrawalForm = () => {
  const [selectedSchedule, setSelectedSchedule] = useState('');
  const [reason, setReason] = useState('');

  // Mock data for approved schedules
  const approvedSchedules = [
    { id: 1, date: '2024-03-10', type: 'Full Day' },
    { id: 2, date: '2024-03-15', type: 'Morning' },
    { id: 3, date: '2024-03-20', type: 'Afternoon' },
  ];

  const handleSubmit = async (e) => {
    e.preventDefault();
    
    // Mock POST request
    try {
      const response = await fetch('/api/withdraw', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ scheduleId: selectedSchedule, reason }),
      });
      
      if (response.ok) {
        alert('Withdrawal submitted successfully');
        setSelectedSchedule('');
        setReason('');
      } else {
        alert('Failed to submit withdrawal');
      }
    } catch (error) {
      console.error('Error submitting withdrawal:', error);
      alert('An error occurred while submitting the withdrawal');
    }
  };

  return (
    <form className="withdrawal-form" onSubmit={handleSubmit}>
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
              {schedule.date} - {schedule.type}
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
      <button type="submit" className="submit-btn">Submit</button>
    </form>
  );
};

export default WithdrawalForm;