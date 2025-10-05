import React, { useState, useEffect } from 'react';
import DashboardHeader from './DashboardHeader';
import CaregiverTable from './CaregiverTable';
import AddCaregiverModal from './AddCaregiverModal';
import { caregiverService } from '../services/caregiverService';

/**
 * Main Caregivers Dashboard component
 * Now integrated with backend API
 */
function CaregiversDashboard() {
  const [caregivers, setCaregivers] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [isAddModalOpen, setIsAddModalOpen] = useState(false);

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

  useEffect(() => {
    fetchCaregivers();
  }, []);

  const handleCaregiverAdded = () => {
    fetchCaregivers(); // Refresh the list after adding
  };

  const handleDeleteCaregiver = async (caregiverId) => {
    try {
      await caregiverService.deleteCaregiver(caregiverId);
      // Refresh the list after successful deletion
      fetchCaregivers();
    } catch (err) {
      console.error('Error deleting caregiver:', err);
      setError(err.message || 'Failed to delete caregiver');
    }
  };

  const handleGeneratePDF = async (caregiverId) => {
    try {
      const pdfBlob = await caregiverService.generateCaregiverPDF(caregiverId);
      
      // Find the caregiver to get their name for the filename
      const caregiver = caregivers.find(c => c.id === caregiverId);
      const caregiverName = caregiver ? caregiver.name.replace(/\s+/g, '-') : caregiverId;
      
      // Create download link for PDF blob
      const url = window.URL.createObjectURL(pdfBlob);
      const link = document.createElement('a');
      link.href = url;
      link.download = `${caregiverName}-report.pdf`;
      document.body.appendChild(link);
      link.click();
      document.body.removeChild(link);
      window.URL.revokeObjectURL(url);
    } catch (err) {
      console.error('Error generating PDF:', err);
      setError(err.message || 'Failed to generate PDF report');
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
      
      {/* Add Caregiver Button */}
      <div className="mb-6">
        <button
          onClick={() => setIsAddModalOpen(true)}
          className="bg-gradient-to-r from-indigo-600 to-purple-600 text-white px-6 py-3 rounded-lg hover:from-indigo-700 hover:to-purple-700 focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:ring-offset-2 shadow-lg hover:shadow-xl transform hover:scale-105 transition-all duration-200 flex items-center font-medium"
        >
          <svg className="w-5 h-5 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 4v16m8-8H4" />
          </svg>
          Add New Caregiver
        </button>
      </div>

      <CaregiverTable caregivers={caregivers} onDelete={handleDeleteCaregiver} onGeneratePDF={handleGeneratePDF} />
      
      {/* Add Caregiver Modal */}
      <AddCaregiverModal
        isOpen={isAddModalOpen}
        onClose={() => setIsAddModalOpen(false)}
        onCaregiverAdded={handleCaregiverAdded}
      />
    </div>
  );
}

export default CaregiversDashboard;
