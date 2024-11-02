import React, { useState, useEffect } from 'react';
import { Link, useParams } from 'react-router-dom';
import axios from 'axios';

const WithdrawalRequests = () => {
  const [requests, setRequests] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const { staffId } = useParams();

  const getShiftType = (is_am, is_pm) => {
    if (is_am && is_pm) return "Full Day";
    if (is_am) return "AM Shift";
    if (is_pm) return "PM Shift";
    return "Unknown";
  };

  const fetchWithdrawalRequests = async () => {
    try {
      const response = await axios.get(`http://localhost:5001/api/team-manager/${staffId}/pending-requests-withdraw`);
      
      // Transform the nested data structure into a flat array of requests
      const allRequests = response.data.team_pending_requests.reduce((acc, member) => {
        const transformedRequests = member.pending_requests.map(request => ({
          ...request,
          type: getShiftType(request.is_am, request.is_pm)
        }));
        return [...acc, ...transformedRequests];
      }, []);

      setRequests(allRequests);
      setLoading(false);
    } catch (err) {
      setError(err.message);
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchWithdrawalRequests();
  }, [staffId]);

  if (loading) {
    return <div>Loading withdrawal requests...</div>;
  }

  if (error) {
    return <div>Error: {error}</div>;
  }

  return (
    <div className="withdrawal-requests-container" style={{ padding: '20px' }}>
      <h1>Pending Withdrawal Requests</h1>
      <table className="withdrawal-requests-table" style={{ width: '100%', borderCollapse: 'collapse' }}>
        <thead>
          <tr>
            <th style={{ padding: '10px', textAlign: 'left', borderBottom: '1px solid #ddd' }}>Request ID</th>
            <th style={{ padding: '10px', textAlign: 'left', borderBottom: '1px solid #ddd' }}>Staff ID</th>
            <th style={{ padding: '10px', textAlign: 'left', borderBottom: '1px solid #ddd' }}>Date</th>
            <th style={{ padding: '10px', textAlign: 'left', borderBottom: '1px solid #ddd' }}>Shift Type</th>
            <th style={{ padding: '10px', textAlign: 'left', borderBottom: '1px solid #ddd' }}>Reason</th>
            <th style={{ padding: '10px', textAlign: 'left', borderBottom: '1px solid #ddd' }}>Action</th>
          </tr>
        </thead>
        <tbody>
          {requests.map((request) => (
            <tr key={request.request_id}>
              <td style={{ padding: '10px', borderBottom: '1px solid #ddd' }}>{request.request_id}</td>
              <td style={{ padding: '10px', borderBottom: '1px solid #ddd' }}>{request.staff_id}</td>
              <td style={{ padding: '10px', borderBottom: '1px solid #ddd' }}>{request.specific_date}</td>
              <td style={{ padding: '10px', borderBottom: '1px solid #ddd' }}>{request.type}</td>
              <td style={{ padding: '10px', borderBottom: '1px solid #ddd' }}>{request.request_reason}</td>
              <td style={{ padding: '10px', borderBottom: '1px solid #ddd' }}>
                <Link to={`/${staffId}/3/withdrawal-approval/${request.staff_id}/${request.request_id}`}>
                  View
                </Link>
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
};

export default WithdrawalRequests;