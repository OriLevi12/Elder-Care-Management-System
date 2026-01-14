import React, { useState, useEffect } from 'react';
import DashboardHeader from './DashboardHeader';
import ElderlyTable from '../tables/ElderlyTable';
import AddElderlyModal from '../modals/AddElderlyModal';
import { elderlyService } from '../../services/elderlyService';

/**
 * Main Elderly Dashboard component
 * Integrated with backend API
 */
function ElderlyDashboard() {
  const [elderly, setElderly] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [isAddModalOpen, setIsAddModalOpen] = useState(false);

  const fetchElderly = async () => {
    try {
      setLoading(true);
      setError(null);
      const data = await elderlyService.getElderly();
      // Sort elderly by ID to maintain consistent order
      const sortedData = data.sort((a, b) => a.id - b.id);
      setElderly(sortedData);
    } catch (err) {
      setError(err.message || 'Failed to fetch elderly');
      console.error('Error fetching elderly:', err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchElderly();
  }, []);

  const handleElderlyAdded = () => {
    fetchElderly(); // Refresh the list after adding
  };

  const handleDeleteElderly = async (elderlyId) => {
    try {
      await elderlyService.deleteElderly(elderlyId);
      // Refresh the list after successful deletion
      fetchElderly();
    } catch (err) {
      console.error('Error deleting elderly:', err);
      setError(err.message || 'Failed to delete elderly');
    }
  };

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
      
      {/* Add Elderly Button */}
      <div className="mb-6">
        <button
          onClick={() => setIsAddModalOpen(true)}
          className="bg-gradient-to-r from-indigo-600 to-purple-600 text-white px-6 py-3 rounded-lg hover:from-indigo-700 hover:to-purple-700 focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:ring-offset-2 shadow-lg hover:shadow-xl transform hover:scale-105 transition-all duration-200 flex items-center font-medium"
        >
          <svg className="w-5 h-5 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 4v16m8-8H4" />
          </svg>
          Add New Elderly
        </button>
      </div>

      <ElderlyTable 
        elderly={elderly} 
        onDelete={handleDeleteElderly}
        onTaskAdded={handleElderlyAdded}
        onMedicationAdded={handleElderlyAdded}
      />
      
      {/* Add Elderly Modal */}
      <AddElderlyModal
        isOpen={isAddModalOpen}
        onClose={() => setIsAddModalOpen(false)}
        onElderlyAdded={handleElderlyAdded}
      />
    </div>
  );
}

export default ElderlyDashboard;
