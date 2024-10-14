import React from 'react';
import { useParams } from 'react-router-dom';
import RequestTable from '../components/RequestsTable/RequestsTable';

const RequestsView = () => {
  const { staffId } = useParams();

  return (
    <div className="requests-view">
      <h1>Requests</h1>
      <RequestTable staffId={staffId} />
    </div>
  );
};

export default RequestsView;