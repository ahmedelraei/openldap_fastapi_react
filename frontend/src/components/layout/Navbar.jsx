import React from 'react';
import { useAuth } from '../../contexts/AuthContext';
import { Link } from 'react-router-dom';
import './Navbar.css';

const Navbar = () => {
  const { user, logout } = useAuth();

  const handleLogout = () => {
    logout();
  };

  return (
    <nav className="navbar">
      <div className="nav-container">
        <Link to="/" className="nav-logo">
          OpenLDAP Auth System
        </Link>
        
        <div className="nav-menu">
          {user ? (
            <>
              <span className="nav-user">
                Welcome, {user.username} ({user.groups.join(', ')})
              </span>
              {user.groups.includes('Group_A') && (
                <Link to="/admin" className="nav-link">Admin Dashboard</Link>
              )}
              {user.groups.includes('Group_B') && (
                <Link to="/user" className="nav-link">User Dashboard</Link>
              )}
              <button onClick={handleLogout} className="nav-button">
                Logout
              </button>
            </>
          ) : (
            <>
              <Link to="/login" className="nav-link">Login</Link>
              <Link to="/register" className="nav-link">Register</Link>
            </>
          )}
        </div>
      </div>
    </nav>
  );
};

export default Navbar;
