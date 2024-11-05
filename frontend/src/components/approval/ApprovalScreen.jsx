import React, { useEffect, useState } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import config from '../../config/config';

const BASE_URL = config.ENDPOINT_BE_URL;

const ApprovalScreen = () => {
  const { staffId, approval_req_id } = useParams();
  const [request, setRequest] = useState(null);
  const [isRecurring, setIsRecurring] = useState(false);
  const [allDates, setAllDates] = useState([]);
  const [loading, setLoading] = useState(true);
  const [decisionNotes, setDecisionNotes] = useState('');
  const [error, setError] = useState(null);
  const navigate = useNavigate();

  const fetchRequestDetails = async () => {
    try {
      const response = await fetch(`${BASE_URL}/api/request/${approval_req_id}`);
      console.log(response);
      
      if (!response.ok) {
        throw new Error('Failed to fetch the request');
      }

      const responseData = await response.json();
      setRequest(responseData.data);  // Changed from data.data to responseData.data
      setIsRecurring(responseData.is_recurring);
      setAllDates(responseData.all_dates);
      setLoading(false);
    } catch (err) {
      setError(err.message);
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchRequestDetails();
  }, [approval_req_id]);

  const formatDayType = (is_am, is_pm) => {
    if (is_am && is_pm) {
      return 'Full Day';
    } else if (is_am) {
      return 'Half Day (AM)';
    } else if (is_pm) {
      return 'Half Day (PM)';
    } else {
      return 'No WFH';
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    const submitter = e.nativeEvent.submitter;
    const decisionStatus = submitter.value;

    try {
      const payload = {
        request_id: approval_req_id,
        decision_status: decisionStatus,
        decision_notes: decisionNotes,
        manager_id: staffId
      };

      const endpoint = isRecurring ? `${BASE_URL}/api/approve_recurring` : `${BASE_URL}/api/approve`;

      const response = await fetch(endpoint, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(payload),
      });

      const result = await response.json();

      if (!response.ok) {
        throw new Error(result.error || 'Failed to process the decision');
      }

      alert(`Decision successfully made: ${decisionStatus}`);
      setError(null);
      navigate(`/${staffId}/3/pending-requests`);
    } catch (error) {
      console.error('Error submitting the decision:', error);
      setError(error.message || 'An error occurred while submitting the decision.');
    }
  };

  if (loading) {
    return <div>Loading...</div>;
  }

  if (error) {
    return <div>Error: {error}</div>;
  }

  return (
    <div style={{ padding: '20px' }}>
      <form onSubmit={handleSubmit} className="approval-form">
        <h2>Approval Screen for Request ID: {approval_req_id}</h2>
        
        <div className="request-details" style={{ marginBottom: '20px' }}>
          <div style={{ 
            backgroundColor: '#f8f9fa', 
            padding: '15px', 
            borderRadius: '4px',
            marginBottom: '20px'
          }}>
            <h3 style={{ marginTop: 0, marginBottom: '10px' }}>Request Details</h3>
            <p><strong>Staff ID:</strong> {request.staff_id}</p>
            <p><strong>Request Type:</strong> {isRecurring ? 'Recurring' : 'Ad-hoc'}</p>
            <p><strong>Current Status:</strong> {request.request_status}</p>
            
            <div style={{ marginBottom: '10px' }}>
              <strong>Requested Date(s):</strong>
              {isRecurring ? (
                <ul style={{ listStyle: 'none', padding: '10px 0', margin: 0 }}>
                  {allDates.map((date, index) => (
                    <li key={index} style={{ marginBottom: '8px' }}>
                      {date.specific_date} - {formatDayType(date.is_am, date.is_pm)}
                    </li>
                  ))}
                </ul>
              ) : (
                <p style={{ margin: '5px 0' }}>
                  {request.specific_date} - {formatDayType(request.is_am, request.is_pm)}
                </p>
              )}
            </div>

            <div>
              <strong>Request Reason:</strong>
              <p style={{ 
                margin: '5px 0',
                padding: '10px',
                backgroundColor: 'white',
                borderRadius: '4px',
                border: '1px solid #dee2e6'
              }}>
                {request.request_reason}
              </p>
            </div>
          </div>
        </div>

        <div className="form-group" style={{ marginBottom: '20px' }}>
          <label style={{ display: 'block', marginBottom: '8px' }}>
            <strong>Decision Notes:</strong>
            <textarea
              value={decisionNotes}
              onChange={(e) => setDecisionNotes(e.target.value)}
              placeholder="Please provide your reason for approval or rejection..."
              style={{ 
                width: '100%', 
                minHeight: '100px',
                padding: '8px',
                marginTop: '8px',
                borderRadius: '4px',
                border: '1px solid #ccc'
              }}
              required
            />
          </label>
        </div>

        <div className="button-group" style={{ display: 'flex', gap: '10px' }}>
          <button 
            type="submit"
            value="Approved"
            style={{ 
              backgroundColor: '#28a745',
              color: 'white', 
              padding: '10px 20px',
              border: 'none',
              borderRadius: '4px',
              cursor: 'pointer'
            }}
          >
            Approve
          </button>
          <button 
            type="submit"
            value="Rejected"
            style={{ 
              backgroundColor: '#dc3545',
              color: 'white',
              padding: '10px 20px',
              border: 'none',
              borderRadius: '4px',
              cursor: 'pointer'
            }}
          >
            Reject
          </button>
        </div>

        {error && (
          <div style={{ 
            marginTop: '20px',
            padding: '10px',
            backgroundColor: '#f8d7da',
            color: '#721c24',
            borderRadius: '4px'
          }}>
            {error}
          </div>
        )}
      </form>
    </div>
  );
};

export default ApprovalScreen;