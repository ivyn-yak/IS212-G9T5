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
      const response = await axios.get(`/api/${staffId}`);
      setRequests(response.data.data);
      setFilteredRequests(response.data.data);
    } catch (error) {
      console.error('Error fetching requests:', error);
      setError('Failed to fetch requests. Please try again later.');
    } finally {
      setIsLoading(false);
    }
  };

  const handleFilter = () => {
    const filtered = requests.filter(request => {
      return (
        (filters.date ? request.start_date === filters.date : true) &&
        (filters.type ? request.request_type === filters.type : true) &&
        (filters.status ? request.request_status === filters.status : true)
      );
    });
    setFilteredRequests(filtered);
  };

  const handleCancel = async (id) => {
    try {
      await axios.post(`/api/cancel-request/${id}`);
      fetchRequests();
    } catch (error) {
      console.error('Error cancelling request:', error);
      setError('Failed to cancel request. Please try again.');
    }
  };

  if (isLoading) {
    return <div>Loading...</div>;
  }

  if (error) {
    return <div>Error: {error}</div>;
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
          value={filters.type}
          onChange={(e) => setFilters({ ...filters, type: e.target.value })}
        >
          <option value="">Select Type</option>
          <option value="Full Day">Full Day</option>
          <option value="Morning">Morning</option>
          <option value="Afternoon">Afternoon</option>
        </select>
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
              <th>Start Date</th>
              <th>End Date</th>
              <th>Type</th>
              <th>Status</th>
              <th>Action</th>
            </tr>
          </thead>
          <tbody>
            {filteredRequests.map((request) => (
              <tr key={request.request_id}>
                <td>{request.request_id}</td>
                <td>{request.start_date}</td>
                <td>{request.end_date}</td>
                <td>{request.request_type}</td>
                <td>{request.request_status}</td>
                <td>
                  {request.request_status === 'Pending' && (
                    <button onClick={() => handleCancel(request.request_id)}>Cancel</button>
                  )}
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      ) : (
        <p>No requests found.</p>
      )}
    </div>
  );
};

export default RequestsTable;