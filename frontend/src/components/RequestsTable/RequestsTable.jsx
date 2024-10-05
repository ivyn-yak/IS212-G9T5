import React, { useState } from 'react';
import './RequestsTable.css';

// Mock data
const mockData = [
  { id: 1, date: '2023-06-25', type: 'Full Day', approvingManager: 'Jack Sim', status: 'Approved' },
  { id: 2, date: '2023-07-28', type: 'Morning', approvingManager: 'Jack Sim', status: 'Rejected' },
  { id: 3, date: '2023-08-15', type: 'Afternoon', approvingManager: 'Jane Doe', status: 'Pending' },
  { id: 4, date: '2023-09-01', type: 'Full Day', approvingManager: 'John Smith', status: 'Withdrawal' },
  { id: 5, date: '2023-09-10', type: 'Morning', approvingManager: 'Jane Doe', status: 'Cancelled' },
];

const RequestsTable = () => {
  const [requests, setRequests] = useState(mockData);
  const [filteredRequests, setFilteredRequests] = useState(mockData);
  const [filters, setFilters] = useState({
    date: '',
    type: '',
    status: '',
  });

  const handleFilter = () => {
    const filtered = requests.filter(request => {
      return (
        (filters.date ? request.date === filters.date : true) &&
        (filters.type ? request.type === filters.type : true) &&
        (filters.status ? request.status === filters.status : true)
      );
    });
    setFilteredRequests(filtered);
  };

  const handleCancel = (id) => {
    console.log(`Cancelling request with id: ${id}`);
    const updatedRequests = requests.map(request =>
      request.id === id ? { ...request, status: 'Cancelled' } : request
    );
    setRequests(updatedRequests);
    setFilteredRequests(updatedRequests);
  };

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
      <table>
        <thead>
          <tr>
            <th>ID</th>
            <th>Date</th>
            <th>Type</th>
            <th>Approving Manager</th>
            <th>Status</th>
            <th>Action</th>
          </tr>
        </thead>
        <tbody>
          {filteredRequests.map((request) => (
            <tr key={request.id}>
              <td>{request.id}</td>
              <td>{request.date}</td>
              <td>{request.type}</td>
              <td>{request.approvingManager}</td>
              <td>{request.status}</td>
              <td>
                {request.status === 'Pending' && (
                  <button onClick={() => handleCancel(request.id)}>Cancel</button>
                )}
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
};

export default RequestsTable;