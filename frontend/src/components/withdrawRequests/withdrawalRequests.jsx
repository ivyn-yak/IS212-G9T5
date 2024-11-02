import React, { useState, useEffect } from 'react';
import { Link, useParams } from 'react-router-dom';
import { getTeamPendingWithdrawals } from '../../api/requests/withdrawRequestsApi';

const WithdrawRequests = () => {
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
      const response = await getTeamPendingWithdrawals(staffId);
      
      // Transform the nested data structure into a flat array of requests
      const allRequests = response.team_pending_requests.reduce((acc, member) => {
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
    <div className="withdrawal-requests-container">
      <h1>Pending Withdrawal Requests</h1>
      <table className="withdrawal-requests-table">
        <thead>
          <tr>
            <th>Request ID</th>
            <th>Staff ID</th>
            <th>Date</th>
            <th>Shift Type</th>
            <th>Reason</th>
            <th>Action</th>
          </tr>
        </thead>
        <tbody>
          {requests.map((request) => (
            <tr key={request.request_id}>
              <td>{request.request_id}</td>
              <td>{request.staff_id}</td>
              <td>{request.specific_date}</td>
              <td>{request.type}</td>
              <td>{request.request_reason}</td>
              <td>
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

export default WithdrawRequests;