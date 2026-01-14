import React from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import { AuthProvider } from './contexts/AuthContext';
import Header from './components/common/header';
import HomePage from './components/dashboards/HomePage';
import CaregiversDashboard from './components/dashboards/CaregiversDashboard';
import ElderlyDashboard from './components/dashboards/ElderlyDashboard';
import Login from './components/auth/Login';
import Register from './components/auth/Register';
import ProtectedRoute from './guards/ProtectedRoute';

function App() {
  return (
    <AuthProvider>
      <Router>
        <div className="min-h-screen bg-gray-50">
          <Routes>
            {/* Public routes */}
            <Route path="/login" element={<Login />} />
            <Route path="/register" element={<Register />} />
            
            {/* Protected routes */}
            <Route path="/" element={
              <ProtectedRoute>
                <Header />
                <HomePage />
              </ProtectedRoute>
            } />
            
            <Route path="/caregiver-dashboard" element={
              <ProtectedRoute>
                <Header />
                <CaregiversDashboard />
              </ProtectedRoute>
            } />
            
            <Route path="/elder-dashboard" element={
              <ProtectedRoute>
                <Header />
                <ElderlyDashboard />
              </ProtectedRoute>
            } />
            
            {/* Catch all route */}
            <Route path="*" element={<Navigate to="/" replace />} />
          </Routes>
        </div>
      </Router>
    </AuthProvider>
  );
}

export default App;