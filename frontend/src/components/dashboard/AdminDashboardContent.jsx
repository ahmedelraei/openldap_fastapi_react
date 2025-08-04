import React, { useState, useEffect } from 'react';
import { useAuth } from '../../contexts/AuthContext';
import axios from 'axios';
import LoadingSpinner from '../ui/LoadingSpinner';
import './Dashboard.css';

const AdminDashboardContent = () => {
  const { user } = useAuth();
  const [users, setUsers] = useState([]);
  const [stats, setStats] = useState({});
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchAdminData();
  }, []);

  const fetchAdminData = async () => {
    try {
      const token = localStorage.getItem('token');
      const headers = token ? { Authorization: `Bearer ${token}` } : {};
      
      const [usersResponse, statsResponse] = await Promise.all([
        axios.get('/admin/users', { headers }),
        axios.get('/admin/stats', { headers })
      ]);
      
      // Ensure we get an array for users
      setUsers(Array.isArray(usersResponse.data) ? usersResponse.data : []);
      setStats(statsResponse.data || {});
    } catch (error) {
      console.error('Failed to fetch admin data:', error);
      // Set empty array on error to prevent map error
      setUsers([]);
      setStats({});
    } finally {
      setLoading(false);
    }
  };

  if (loading) {
    return <LoadingSpinner message="Loading admin dashboard..." />;
  }

  return (
    <div className="dashboard">
      <div className="dashboard-header">
        <h1>Admin Dashboard</h1>
        <p>Welcome back, {user.username}! You have administrative privileges.</p>
      </div>

      <div className="dashboard-content">
        <div className="stats-grid">
          <div className="stat-card">
            <h3>Total Users</h3>
            <p className="stat-number">{stats.total_users || 0}</p>
          </div>
          <div className="stat-card">
            <h3>Group A Users</h3>
            <p className="stat-number">{stats.group_a_users || 0}</p>
          </div>
          <div className="stat-card">
            <h3>Group B Users</h3>
            <p className="stat-number">{stats.group_b_users || 0}</p>
          </div>
          <div className="stat-card">
            <h3>Active Sessions</h3>
            <p className="stat-number">{stats.active_sessions || 0}</p>
          </div>
        </div>

        <div className="users-section">
          <h2>User Management</h2>
          <div className="users-table-container">
            <table className="users-table">
              <thead>
                <tr>
                  <th>Username</th>
                  <th>Email</th>
                  <th>Groups</th>
                  <th>Created At</th>
                  <th>Last Login</th>
                </tr>
              </thead>
              <tbody>
                {Array.isArray(users) && users.length > 0 ? (
                  users.map((user, index) => (
                    <tr key={index}>
                      <td>{user.username}</td>
                      <td>{user.email}</td>
                      <td>{Array.isArray(user.groups) ? user.groups.join(', ') : 'No groups'}</td>
                      <td>{user.created_at ? new Date(user.created_at).toLocaleDateString() : 'N/A'}</td>
                      <td>{user.last_login ? new Date(user.last_login).toLocaleDateString() : 'Never'}</td>
                    </tr>
                  ))
                ) : (
                  <tr>
                    <td colSpan="5" className="text-center">No users found</td>
                  </tr>
                )}
              </tbody>
            </table>
          </div>
        </div>
      </div>
    </div>
  );
};

export default AdminDashboardContent;
