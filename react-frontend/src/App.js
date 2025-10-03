import React from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import { AuthProvider } from './contexts/AuthContext';
import Header from './components/header';
import CaregiversDashboard from './components/CaregiversDashboard';
import Login from './components/Login';
import Register from './components/Register';
import ProtectedRoute from './components/ProtectedRoute';

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
                <main className="container mx-auto px-6 py-8">
                  <h1 className="text-3xl font-bold text-gray-800 mb-6">
                    Welcome to Elder Care Manager
                  </h1>
                  <p className="text-lg text-gray-600">
                    Manage your caregivers, elderly clients, and tasks efficiently.
                  </p>
                </main>
              </ProtectedRoute>
            } />
            
            <Route path="/caregiver-dashboard" element={
              <ProtectedRoute>
                <Header />
                <CaregiversDashboard />
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