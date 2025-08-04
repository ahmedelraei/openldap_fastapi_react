import React from 'react';
import { Navigate } from 'react-router-dom';
import { useAuth } from '../../contexts/AuthContext';

const DashboardRedirect = () => {
  const { user } = useAuth();
  
  if (user.groups.includes('Group_A')) {
    return <Navigate to="/admin" />;
  } else if (user.groups.includes('Group_B')) {
    return <Navigate to="/user" />;
  } else {
    return (
      <div className="error-container">
        <h2>Access Error</h2>
        <p>No appropriate dashboard found for your user group.</p>
      </div>
    );
  }
};

export default DashboardRedirect;
