import React, { useState } from 'react';
import { useParams, useNavigate, useLocation } from 'react-router-dom';
import { processWithdrawalDecision } from '../../api/requests/withdrawRequestsApi';
import './WithdrawalApprovalScreen.css';

const WithdrawalApprovalScreen = () => {
  const { staffId, approval_staff_id, withdrawal_id } = useParams();
  const location = useLocation();
  const { request } = location.state || {};
  const [decisionNotes, setDecisionNotes] = useState('');
  const [error, setError] = useState(null);
  const [isSubmitting, setIsSubmitting] = useState(false);
  const navigate = useNavigate();

  const handleDecision = async (decisionStatus) => {
    if (!decisionNotes.trim()) {
      setError('Decision notes are required');
      return;
    }

    setIsSubmitting(true);
    setError(null);

    try {
      const payload = {
        request_id: withdrawal_id,
        specific_date: request.specific_date,
        manager_id: staffId,
        decision_status: decisionStatus,
        decision_notes: decisionNotes.trim()
      };

      const response = await processWithdrawalDecision(payload);
      
      alert(`Withdrawal request ${decisionStatus.toLowerCase()} successfully`);
      navigate(`/${staffId}/3/withdrawal-requests`);
    } catch (error) {
      console.error('Error processing withdrawal decision:', error);
      setError(error.message);
    } finally {
      setIsSubmitting(false);
    }
  };

  if (!request) return <div className="approval-screen-error">Request not found</div>;

  return (
    <div className="approval-screen-container">
      <h2>Withdrawal Request Approval</h2>
      <div className="request-details">
        <h3>Request Details:</h3>
        <p><strong>Reference Request ID:</strong> {request.request_id}</p>
        <p><strong>Staff ID:</strong> {request.staff_id}</p>
        <p><strong>Date:</strong> {request.specific_date}</p>
        <p><strong>Type:</strong> {request.type}</p>
        <p><strong>Staff's Reason:</strong> {request.request_reason}</p>
      </div>
      
      {error && (
        <div className="error-message">
          {error}
        </div>
      )}

      <div className="decision-notes">
        <label>
          Decision Notes:
          <textarea
            value={decisionNotes}
            onChange={(e) => setDecisionNotes(e.target.value)}
            placeholder="Add your reason for approval/rejection (required)"
            required
            disabled={isSubmitting}
          />
        </label>
      </div>

      <div className="decision-buttons">
        <button 
          onClick={() => handleDecision('Approved')}
          className="approve-button"
          disabled={isSubmitting}
        >
          {isSubmitting ? 'Processing...' : 'Approve'}
        </button>
        <button 
          onClick={() => handleDecision('Rejected')}
          className="reject-button"
          disabled={isSubmitting}
        >
          {isSubmitting ? 'Processing...' : 'Reject'}
        </button>
      </div>
    </div>
  );
};

export default WithdrawalApprovalScreen;