import React, { useState, useEffect } from 'react';
import { useAuth } from '../../contexts/AuthContext';
import axios from 'axios';
import LoadingSpinner from '../ui/LoadingSpinner';
import './Dashboard.css';

const UserDashboardContent = () => {
  const { user } = useAuth();
  const [profile, setProfile] = useState({});
  const [activities, setActivities] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchUserData();
  }, []);

  const fetchUserData = async () => {
    try {
      const [profileResponse, activitiesResponse] = await Promise.all([
        axios.get('/user/profile'),
        axios.get('/user/activities')
      ]);
      
      setProfile(profileResponse.data);
      setActivities(activitiesResponse.data);
    } catch (error) {
      console.error('Failed to fetch user data:', error);
    } finally {
      setLoading(false);
    }
  };

  if (loading) {
    return <LoadingSpinner message="Loading user dashboard..." />;
  }

  return (
    <div className="dashboard">
      <div className="dashboard-header">
        <h1>User Dashboard</h1>
        <p>Welcome, {user.username}! Here's your personal workspace.</p>
      </div>

      <div className="dashboard-content">
        <div className="profile-section">
          <h2>Profile Information</h2>
          <div className="profile-card">
            <div className="profile-item">
              <label>Username:</label>
              <span>{profile.username || user.username}</span>
            </div>
            <div className="profile-item">
              <label>Email:</label>
              <span>{profile.email || 'Not provided'}</span>
            </div>
            <div className="profile-item">
              <label>Groups:</label>
              <span>{user.groups.join(', ')}</span>
            </div>
            <div className="profile-item">
              <label>Member Since:</label>
              <span>{profile.created_at ? new Date(profile.created_at).toLocaleDateString() : 'Unknown'}</span>
            </div>
            <div className="profile-item">
              <label>Last Login:</label>
              <span>{profile.last_login ? new Date(profile.last_login).toLocaleString() : 'This session'}</span>
            </div>
          </div>
        </div>

        <div className="activities-section">
          <h2>Recent Activities</h2>
          <div className="activities-list">
            {activities.length > 0 ? (
              activities.map((activity, index) => (
                <div key={index} className="activity-item">
                  <div className="activity-time">
                    {new Date(activity.timestamp).toLocaleString()}
                  </div>
                  <div className="activity-description">
                    {activity.description}
                  </div>
                </div>
              ))
            ) : (
              <p className="no-activities">No recent activities found.</p>
            )}
          </div>
        </div>

        <div className="user-stats">
          <h2>Your Statistics</h2>
          <div className="stats-grid">
            <div className="stat-card">
              <h3>Login Count</h3>
              <p className="stat-number">{profile.login_count || 0}</p>
            </div>
            <div className="stat-card">
              <h3>Days Active</h3>
              <p className="stat-number">{profile.days_active || 0}</p>
            </div>
            <div className="stat-card">
              <h3>Last Activity</h3>
              <p className="stat-text">
                {profile.last_activity ? new Date(profile.last_activity).toLocaleDateString() : 'Today'}
              </p>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default UserDashboardContent;
