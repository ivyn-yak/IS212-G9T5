import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';

const PendingRequests = () => {
  const [requests, setRequests] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  const fetchAllRequests = async (staffIds) => {
    try {
      const allRequests = [];
      
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
      
      for (const staffId of staffIds) {
        const data = mockData[staffId] || [];
        allRequests.push(...data);
      }
  
      setRequests(allRequests);
      setLoading(false);
    } catch (err) {
      setError(err.message);
      setLoading(false);
    }
  };

  const groupRequestsByRequestId = (requests) => {
    const groupedRequests = {};
    
    requests.forEach((request) => {
      if (!groupedRequests[request.request_id]) {
        groupedRequests[request.request_id] = {
          request_id: request.request_id,
          staff_id: request.staff_id,
          dates: [request.specific_date],
        };
      } else {
        groupedRequests[request.request_id].dates.push(request.specific_date);
      }
    });
    
    return Object.values(groupedRequests);
  };

  useEffect(() => {
    const staffIds = [1, 2];
    fetchAllRequests(staffIds);
  }, []);

  if (loading) {
    return <div>Loading pending requests...</div>;
  }

  if (error) {
    return <div>Error: {error}</div>;
  }

  const groupedRequests = groupRequestsByRequestId(requests);

  return (
    <div className="pending-requests-container" style={{ padding: '20px' }}>
      <h2>Attendance</h2>
      <h3>Pending / Pending Requests</h3>
      <table className="pending-requests-table" style={{ width: '100%', borderCollapse: 'collapse' }}>
        <thead>
          <tr>
            <th style={{ padding: '10px', textAlign: 'left', borderBottom: '1px solid #ddd' }}>Request ID</th>
            <th style={{ padding: '10px', textAlign: 'left', borderBottom: '1px solid #ddd' }}>Specific Date(s)</th>
            <th style={{ padding: '10px', textAlign: 'left', borderBottom: '1px solid #ddd' }}>Action</th>
          </tr>
        </thead>
        <tbody>
          {groupedRequests.map((request) => (
            <tr key={request.request_id}>
              <td style={{ padding: '10px', borderBottom: '1px solid #ddd' }}>{request.request_id}</td>
              <td style={{ padding: '10px', borderBottom: '1px solid #ddd' }}>
                {request.dates.map((date, index) => (
                  <span key={index}>
                    {date}
                    {index !== request.dates.length - 1 && <br />}
                  </span>
                ))}
              </td>
              <td style={{ padding: '10px', borderBottom: '1px solid #ddd' }}>
                <Link to={`/Manager/ApprovalScreen/${request.staff_id}`}>
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

export default PendingRequests;




