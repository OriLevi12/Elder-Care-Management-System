import React, { useState } from 'react';
import { caregiverService } from '../../services/caregiverService';

/**
 * Modal component for adding a new caregiver
 */
const AddCaregiverModal = ({ isOpen, onClose, onCaregiverAdded }) => {
  const [formData, setFormData] = useState({
    custom_id: '',
    name: '',
    bank_name: '',
    bank_account: '',
    branch_number: ''
  });
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const handleInputChange = (e) => {
    const { name, value } = e.target;
    setFormData(prev => ({
      ...prev,
      [name]: value
    }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    
    // Basic validation
    if (!formData.custom_id || !formData.name || !formData.bank_name || !formData.bank_account || !formData.branch_number) {
      setError('All fields are required');
      return;
    }

    try {
      setLoading(true);
      setError(null);
      
      // Convert custom_id to number
      const caregiverData = {
        ...formData,
        custom_id: parseInt(formData.custom_id)
      };
      
      await caregiverService.addCaregiver(caregiverData);
      
      // Reset form and close modal
      setFormData({
        custom_id: '',
        name: '',
        bank_name: '',
        bank_account: '',
        branch_number: ''
      });
      
      onCaregiverAdded(); // Refresh the caregiver list
      onClose();
      
    } catch (err) {
      setError(err.message || 'Failed to add caregiver');
      console.error('Error adding caregiver:', err);
    } finally {
      setLoading(false);
    }
  };

  const handleClose = () => {
    setFormData({
      custom_id: '',
      name: '',
      bank_name: '',
      bank_account: '',
      branch_number: ''
    });
    setError(null);
    onClose();
  };

  if (!isOpen) return null;

  return (
    <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
      <div className="bg-white rounded-lg shadow-xl max-w-md w-full mx-4">
        {/* Header */}
        <div className="px-6 py-4 border-b border-gray-200">
          <div className="flex justify-between items-center">
            <h2 className="text-xl font-semibold text-gray-800">Add New Caregiver</h2>
            <button
              onClick={handleClose}
              className="text-gray-400 hover:text-gray-600 text-2xl"
            >
              ×
            </button>
          </div>
        </div>

        {/* Form */}
        <form onSubmit={handleSubmit} className="px-6 py-4">
          <div className="space-y-4">
            {/* Custom ID */}
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">
                Caregiver ID *
              </label>
              <input
                type="number"
                name="custom_id"
                value={formData.custom_id}
                onChange={handleInputChange}
                className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-indigo-500"
                placeholder="Enter caregiver ID"
                required
              />
            </div>

            {/* Name */}
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">
                Full Name *
              </label>
              <input
                type="text"
                name="name"
                value={formData.name}
                onChange={handleInputChange}
                className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-indigo-500"
                placeholder="Enter full name"
                required
              />
            </div>

            {/* Bank Name */}
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">
                Bank Name *
              </label>
              <input
                type="text"
                name="bank_name"
                value={formData.bank_name}
                onChange={handleInputChange}
                className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-indigo-500"
                placeholder="Enter bank name"
                required
              />
            </div>

            {/* Bank Account */}
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">
                Bank Account *
              </label>
              <input
                type="text"
                name="bank_account"
                value={formData.bank_account}
                onChange={handleInputChange}
                className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-indigo-500"
                placeholder="Enter bank account number"
                required
              />
            </div>

            {/* Branch Number */}
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">
                Branch Number *
              </label>
              <input
                type="text"
                name="branch_number"
                value={formData.branch_number}
                onChange={handleInputChange}
                className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-indigo-500"
                placeholder="Enter branch number"
                required
              />
            </div>
          </div>

          {/* Error Message */}
          {error && (
            <div className="mt-4 bg-red-50 border border-red-200 rounded-md p-3">
              <div className="text-red-700 text-sm">{error}</div>
            </div>
          )}

          {/* Buttons */}
          <div className="flex space-x-3 mt-6">
            <button
              type="button"
              onClick={handleClose}
              className="flex-1 bg-gray-300 text-gray-700 py-2 px-4 rounded-md hover:bg-gray-400 focus:outline-none focus:ring-2 focus:ring-gray-500"
            >
              Cancel
            </button>
            <button
              type="submit"
              disabled={loading}
              className="flex-1 bg-indigo-600 text-white py-2 px-4 rounded-md hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-indigo-500 disabled:opacity-50"
            >
              {loading ? 'Adding...' : 'Add Caregiver'}
            </button>
          </div>
        </form>
      </div>
    </div>
  );
};

export default AddCaregiverModal;
