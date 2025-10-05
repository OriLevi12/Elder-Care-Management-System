import React, { useState } from 'react';
import { caregiverService } from '../services/caregiverService';

const UpdateSalaryModal = ({ caregiver, isOpen, onClose, onSalaryUpdated }) => {
  const [formData, setFormData] = useState({
    salary_price: caregiver.salary?.price || 0,
    salary_amount: caregiver.salary?.amount || 0,
    saturday_price: caregiver.saturday?.price || 0,
    saturday_amount: caregiver.saturday?.amount || 0,
    allowance_price: caregiver.allowance?.price || 0,
    allowance_amount: caregiver.allowance?.amount || 0,
  });
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData({ ...formData, [name]: parseFloat(value) || 0 });
    setError('');
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError('');
    setLoading(true);

    // Basic validation
    if (formData.salary_price < 0 || formData.salary_amount < 0 || formData.saturday_price < 0 || formData.saturday_amount < 0 || formData.allowance_price < 0 || formData.allowance_amount < 0) {
      setError('Salary values cannot be negative.');
      setLoading(false);
      return;
    }

    try {
      await caregiverService.updateCaregiverSalary(caregiver.id, formData);
      onClose(); // Close modal
      onSalaryUpdated(); // Refresh list
    } catch (err) {
      setError(err.message || 'Failed to update salary.');
      console.error('Error updating salary:', err);
    } finally {
      setLoading(false);
    }
  };

  if (!isOpen) return null;

  return (
    <div className="fixed inset-0 bg-gray-600 bg-opacity-50 overflow-y-auto h-full w-full z-50 flex justify-center items-center">
      <div className="relative p-8 bg-white w-full max-w-md mx-auto rounded-lg shadow-lg">
        <button 
          onClick={onClose} 
          className="absolute top-4 right-4 text-gray-500 hover:text-gray-700 text-xl"
        >
          ×
        </button>
        
        <h2 className="text-2xl font-bold text-gray-800 mb-6 text-center">
          Update Salary - {caregiver.name}
        </h2>
        
        {error && (
          <div className="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded relative mb-4">
            {error}
          </div>
        )}
        
        <form onSubmit={handleSubmit} className="space-y-4">
          {/* Salary Section */}
          <div className="border rounded-lg p-4 bg-blue-50">
            <h3 className="text-lg font-medium text-blue-800 mb-3">Salary</h3>
            <div className="grid grid-cols-2 gap-4">
              <div>
                <label htmlFor="salary_price" className="block text-sm font-medium text-gray-700">
                  Salary Price (₪)
                </label>
                <input
                  type="number"
                  id="salary_price"
                  name="salary_price"
                  value={formData.salary_price}
                  onChange={handleChange}
                  min="0"
                  step="0.01"
                  required
                  className="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm"
                />
              </div>
              <div>
                <label htmlFor="salary_amount" className="block text-sm font-medium text-gray-700">
                  Salary Amount
                </label>
                <input
                  type="number"
                  id="salary_amount"
                  name="salary_amount"
                  value={formData.salary_amount}
                  onChange={handleChange}
                  min="0"
                  required
                  className="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm"
                />
              </div>
            </div>
          </div>
          
          {/* Saturday Section */}
          <div className="border rounded-lg p-4 bg-red-50">
            <h3 className="text-lg font-medium text-red-800 mb-3">Saturday</h3>
            <div className="grid grid-cols-2 gap-4">
              <div>
                <label htmlFor="saturday_price" className="block text-sm font-medium text-gray-700">
                  Saturday Price (₪)
                </label>
                <input
                  type="number"
                  id="saturday_price"
                  name="saturday_price"
                  value={formData.saturday_price}
                  onChange={handleChange}
                  min="0"
                  step="0.01"
                  required
                  className="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm"
                />
              </div>
              <div>
                <label htmlFor="saturday_amount" className="block text-sm font-medium text-gray-700">
                  Saturday Amount
                </label>
                <input
                  type="number"
                  id="saturday_amount"
                  name="saturday_amount"
                  value={formData.saturday_amount}
                  onChange={handleChange}
                  min="0"
                  required
                  className="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm"
                />
              </div>
            </div>
          </div>
          
          {/* Allowance Section */}
          <div className="border rounded-lg p-4 bg-green-50">
            <h3 className="text-lg font-medium text-green-800 mb-3">Allowance</h3>
            <div className="grid grid-cols-2 gap-4">
              <div>
                <label htmlFor="allowance_price" className="block text-sm font-medium text-gray-700">
                  Allowance Price (₪)
                </label>
                <input
                  type="number"
                  id="allowance_price"
                  name="allowance_price"
                  value={formData.allowance_price}
                  onChange={handleChange}
                  min="0"
                  step="0.01"
                  required
                  className="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm"
                />
              </div>
              <div>
                <label htmlFor="allowance_amount" className="block text-sm font-medium text-gray-700">
                  Allowance Amount
                </label>
                <input
                  type="number"
                  id="allowance_amount"
                  name="allowance_amount"
                  value={formData.allowance_amount}
                  onChange={handleChange}
                  min="0"
                  required
                  className="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm"
                />
              </div>
            </div>
          </div>
          
          <div className="bg-gray-50 p-4 rounded-md">
            <h3 className="text-sm font-medium text-gray-700 mb-2">Total Salary Preview</h3>
            <div className="text-lg font-semibold text-green-600">
              ₪{(formData.salary_price * formData.salary_amount + formData.saturday_price * formData.saturday_amount + formData.allowance_price * formData.allowance_amount).toFixed(2)}
            </div>
          </div>
          
          <div className="flex justify-end space-x-3 mt-6">
            <button
              type="button"
              onClick={onClose}
              className="px-4 py-2 border border-gray-300 rounded-md shadow-sm text-sm font-medium text-gray-700 hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500"
            >
              Cancel
            </button>
            <button
              type="submit"
              disabled={loading}
              className="px-4 py-2 bg-indigo-600 border border-transparent rounded-md shadow-sm text-sm font-medium text-white hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500 disabled:opacity-50 disabled:cursor-not-allowed"
            >
              {loading ? 'Updating...' : 'Update Salary'}
            </button>
          </div>
        </form>
      </div>
    </div>
  );
};

export default UpdateSalaryModal;
