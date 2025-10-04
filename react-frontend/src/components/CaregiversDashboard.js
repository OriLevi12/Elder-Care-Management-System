import React, { useState, useEffect } from 'react';
import DashboardHeader from './DashboardHeader';
import CaregiverTable from './CaregiverTable';
import { caregiverService } from '../services/caregiverService';

/**
 * Main Caregivers Dashboard component
 * Now integrated with backend API
 */
function CaregiversDashboard() {
  const [caregivers, setCaregivers] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchCaregivers = async () => {
      try {
        setLoading(true);
        setError(null);
        const data = await caregiverService.getCaregivers();
        setCaregivers(data);
      } catch (err) {
        setError(err.message || 'Failed to fetch caregivers');
        console.error('Error fetching caregivers:', err);
      } finally {
        setLoading(false);
      }
    };

    fetchCaregivers();
  }, []);

  if (loading) {
    return (
      <div className="container mx-auto p-6 max-w-6xl">
        <DashboardHeader />
        <div className="flex justify-center items-center h-64">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-indigo-600"></div>
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="container mx-auto p-6 max-w-6xl">
        <DashboardHeader />
        <div className="bg-red-50 border border-red-200 rounded-md p-4">
          <div className="text-red-700">Error: {error}</div>
        </div>
      </div>
    );
  }

  return (
    <div className="container mx-auto p-6 max-w-6xl">
      <DashboardHeader />
      <CaregiverTable caregivers={caregivers} />
    </div>
  );
}

export default CaregiversDashboard;
