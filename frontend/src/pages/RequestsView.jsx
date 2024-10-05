import React from 'react';
import RequestTable from '../components/RequestsTable/RequestsTable';

const RequestsView = () => {
  return (
    <div className="requests-view">
      <h1>Requests</h1>
      <RequestTable />
    </div>
  );
};

export default RequestsView;