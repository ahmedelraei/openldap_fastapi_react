import React, { Suspense, lazy } from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import { AuthProvider } from './contexts/AuthContext';
import Navbar from './components/layout/Navbar';
import ProtectedRoute from './components/common/ProtectedRoute';
import DashboardRedirect from './components/common/DashboardRedirect';
import LoadingSpinner from './components/ui/LoadingSpinner';
import ProxyDebug from './components/debug/ProxyDebug';
import './styles/App.css';
import './styles/globals.css';

// Lazy load pages for better performance
const LoginPage = lazy(() => import('./pages/LoginPage'));
const RegisterPage = lazy(() => import('./pages/RegisterPage'));
const AdminDashboardPage = lazy(() => import('./pages/AdminDashboardPage'));
const UserDashboardPage = lazy(() => import('./pages/UserDashboardPage'));

function App() {
  return (
    <AuthProvider>
      <Router>
        <div className="App">
          <Navbar />
          <main className="main-content">
            <Suspense fallback={<LoadingSpinner size="large" message="Loading page..." />}>
              <Routes>
                <Route path="/debug" element={<ProxyDebug />} />
                <Route path="/login" element={<LoginPage />} />
                <Route path="/register" element={<RegisterPage />} />
                <Route 
                  path="/admin" 
                  element={
                    <ProtectedRoute requiredGroup="Group_A">
                      <AdminDashboardPage />
                    </ProtectedRoute>
                  } 
                />
                <Route 
                  path="/user" 
                  element={
                    <ProtectedRoute requiredGroup="Group_B">
                      <UserDashboardPage />
                    </ProtectedRoute>
                  } 
                />
                <Route 
                  path="/dashboard" 
                  element={
                    <ProtectedRoute>
                      <DashboardRedirect />
                    </ProtectedRoute>
                  } 
                />
                <Route path="/" element={<Navigate to="/dashboard" />} />
              </Routes>
            </Suspense>
          </main>
        </div>
      </Router>
    </AuthProvider>
  );
}

export default App;
