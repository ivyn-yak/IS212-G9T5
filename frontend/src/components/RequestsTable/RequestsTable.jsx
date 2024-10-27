import React, { useState, useEffect } from 'react';
import axios from 'axios';
import './RequestsTable.css';

const RequestsTable = ({ staffId }) => {
  const [requests, setRequests] = useState([]);
  const [filteredRequests, setFilteredRequests] = useState([]);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState(null);
  const [filters, setFilters] = useState({
    date: '',
    type: '',
    status: '',
  });

  useEffect(() => {
    fetchRequests();
  }, [staffId]);

  const fetchRequests = async () => {
    setIsLoading(true);
    setError(null);
    try {
      const response = await axios.get(`http://localhost:5001/api/staff/${staffId}/all_wfh_dates`);
      setRequests(response.data);
      setFilteredRequests(response.data);
    } catch (error) {
      console.error('Error fetching requests:', error);
      if (error.response && error.response.status === 404) {
        setError('No WFH requests found for this staff member.');
      } else {
        setError('Failed to fetch requests. Please try again later.');
      }
    } finally {
      setIsLoading(false);
    }
  };

  const handleFilter = () => {
    const filtered = requests.filter(request => {
      return (
        (filters.date ? request.specific_date === filters.date : true) &&
        (filters.status ? request.request_status === filters.status : true)
      );
    });
    setFilteredRequests(filtered);
  };

  const handleCancel = async (request_id, specific_date, staff_id) => {
    try {
      // await axios.post(`/api/cancel-request/${id}`);
      console.log('Request cancelled:', request_id, specific_date, staff_id);
      // fetchRequests();
    } catch (error) {
      console.error('Error cancelling request:', error);
      setError('Failed to cancel request. Please try again.');
    }
  };

  if (isLoading) {
    return <div>Loading...</div>;
  }

  // If there's an error but it's the "No requests found" message,
  // we'll show it in a more user-friendly way
  if (error === 'No WFH requests found for this staff member.') {
    return (
      <div className="request-table">
        <div className="filter-section">
          <input
            type="date"
            value={filters.date}
            onChange={(e) => setFilters({ ...filters, date: e.target.value })}
          />
          <select
            value={filters.status}
            onChange={(e) => setFilters({ ...filters, status: e.target.value })}
          >
            <option value="">Select Status</option>
            <option value="Approved">Approved</option>
            <option value="Rejected">Rejected</option>
            <option value="Withdrawal">Withdrawal</option>
            <option value="Cancelled">Cancelled</option>
            <option value="Pending">Pending</option>
          </select>
          <button onClick={handleFilter}>Filter</button>
        </div>
        <p className="no-requests-message">{error}</p>
      </div>
    );
  }

  // For other types of errors, show the error message
  if (error) {
    return <div className="error-message">Error: {error}</div>;
  }

  return (
    <div className="request-table">
      <div className="filter-section">
        <input
          type="date"
          value={filters.date}
          onChange={(e) => setFilters({ ...filters, date: e.target.value })}
        />
        <select
          value={filters.status}
          onChange={(e) => setFilters({ ...filters, status: e.target.value })}
        >
          <option value="">Select Status</option>
          <option value="Approved">Approved</option>
          <option value="Rejected">Rejected</option>
          <option value="Withdrawal">Withdrawal</option>
          <option value="Cancelled">Cancelled</option>
          <option value="Pending">Pending</option>
        </select>
        <button onClick={handleFilter}>Filter</button>
      </div>
      {Array.isArray(filteredRequests) && filteredRequests.length > 0 ? (
        <table>
          <thead>
            <tr>
              <th>ID</th>
              <th>Date</th>
              <th>Status</th>
              <th>Action</th>
            </tr>
          </thead>
          <tbody>
            {filteredRequests.map((request) => (
              <tr key={request.request_id}>
                <td>{request.request_id}</td>
                <td>{request.specific_date}</td>
                <td>{request.request_status}</td>
                <td>
                  {request.request_status === 'Pending' ? (
                    <button onClick={() => handleCancel(request.request_id, request.specific_date, staffId)}>Cancel</button>
                  ) : (
                    'No Actions Available'
                  )}
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      ) : (
        <p>No requests match your filter criteria.</p>
      )}
    </div>
  );
};

export default RequestsTable;