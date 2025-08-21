import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import Header from './components/header';
import CaregiverDashboard from './components/CaregiverDashboard';

function App() {
  return (
    <Router>
      <div className="min-h-screen bg-gray-50">
        <Header />
        <Routes>
          <Route path="/" element={
            <main className="container mx-auto px-6 py-8">
              <h1 className="text-3xl font-bold text-gray-800 mb-6">
                Welcome to Elder Care Manager
              </h1>
              <p className="text-lg text-gray-600">
                Manage your caregivers, elderly clients, and tasks efficiently.
              </p>
            </main>
          } />
          <Route path="/caregiver-dashboard" element={<CaregiverDashboard />} />
        </Routes>
      </div>
    </Router>
  );
}

export default App;