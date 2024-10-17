import React, { useEffect, useState } from 'react';
import { useParams, useNavigate } from 'react-router-dom';

const ApprovalScreen = () => {
  const { staff_id } = useParams();  // Get staff_id from the URL (passed from PendingRequests)
  const [requests, setRequests] = useState([]);
  const [loading, setLoading] = useState(true);
  const [decisionNotes, setDecisionNotes] = useState('');  // State to handle the reason for approval/rejection
  const [error, setError] = useState(null);
  const navigate = useNavigate(); // To redirect after successful approval/rejection

  // Simulated data for staff requests (mock data based on staff_id)
  const mockData = {
    1: [
      { date_id: 1, request_id: 101, staff_id: 1, specific_date: '2024-10-01', is_am: true, is_pm: false },
      { date_id: 2, request_id: 101, staff_id: 1, specific_date: '2024-10-02', is_am: true, is_pm: true },
    ],
    2: [
      { date_id: 3, request_id: 103, staff_id: 2, specific_date: '2024-10-01', is_am: false, is_pm: true },
      { date_id: 4, request_id: 104, staff_id: 2, specific_date: '2024-10-03', is_am: true, is_pm: true },
    ],
  };

  // Fetch the WFH requests for a specific staff member
  const fetchStaffRequests = async (staffId) => {
    try {
      const data = mockData[staffId] || []; // Use mock data for requests
      setRequests(data);
      setLoading(false);
    } catch (err) {
      setError(err.message);
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchStaffRequests(staff_id); // Fetch requests based on the staff_id passed in the URL
  }, [staff_id]);

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

  const handleDecision = async (decisionStatus) => {
    try {
      // Build the payload to be sent to the backend
      const payload = {
        request_id: requests[0]?.request_id, // Assuming all requests have the same request_id
        manager_id: 1, // Replace with the logged-in manager's ID
        decision_status: decisionStatus, // "approved" or "rejected"
        decision_notes: decisionNotes,  // Include the reason for approval/rejection
      };

      console.log('Payload that will be sent:', payload);

      // Simulate successful action after approval/rejection
      alert(`Decision successfully made: ${decisionStatus}`);
      setError(null);  // Clear any existing errors

      // Redirect to the pending requests page after the mock success
      navigate("/Manager/PendingRequests");

    } catch (error) {
      console.error('Error submitting the decision:', error);
      setError('An error occurred while submitting the decision.');
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
      <h2>Approval Screen for Staff ID: {staff_id}</h2>
      <p>Reference Request ID: {requests[0]?.request_id}</p>
      <div>
        <h3>Requested Dates:</h3>
        <ul>
          {requests.map((req) => (
            <li key={req.date_id}>
              {req.specific_date} - {formatDayType(req.is_am, req.is_pm)}
            </li>
          ))}
        </ul>
      </div>
      <div>
        <label>
          Reason for Approval/Rejection:
          <textarea
            value={decisionNotes}
            onChange={(e) => setDecisionNotes(e.target.value)}
            placeholder="Add your reason here..."
            style={{ width: '100%', minHeight: '100px' }}  // Adjust styling as needed
          />
        </label>
      </div>
      <div>
        <button onClick={() => handleDecision('approved')} style={{ backgroundColor: 'green', color: 'white', marginRight: '10px' }}>
          Approve
        </button>
        <button onClick={() => handleDecision('rejected')} style={{ backgroundColor: 'red', color: 'white' }}>
          Reject
        </button>
      </div>
      {error && <p style={{ color: 'red' }}>{error}</p>}
    </div>
  );
};

export default ApprovalScreen;


