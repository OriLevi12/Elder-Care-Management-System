import React, { useState, useEffect } from 'react';
import assignmentService from '../services/assignmentService';

const AssignmentModal = ({ isOpen, onClose, caregiverId, caregiverName, onAssignmentChanged }) => {
  const [elderly, setElderly] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [isRemoving, setIsRemoving] = useState(null);

  useEffect(() => {
    if (isOpen && caregiverId) {
      fetchElderlyForCaregiver();
    }
  }, [isOpen, caregiverId]);

  const fetchElderlyForCaregiver = async () => {
    setLoading(true);
    setError(null);
    
    try {
      const elderlyList = await assignmentService.getElderlyForCaregiver(caregiverId);
      setElderly(elderlyList);
    } catch (err) {
      console.error('Error fetching elderly for caregiver:', err);
      setError(err.message || 'Failed to load elderly assignments');
    } finally {
      setLoading(false);
    }
  };

  const handleClose = () => {
    setElderly([]);
    setError(null);
    onClose();
  };

  const handleRemoveAssignment = async (elderlyId) => {
    setIsRemoving(elderlyId);
    try {
      await assignmentService.deleteAssignment(caregiverId, elderlyId);
      
      // Refresh data
      await fetchElderlyForCaregiver();
      
      // Notify parent component
      if (onAssignmentChanged) {
        onAssignmentChanged();
      }
    } catch (err) {
      console.error('Error removing assignment:', err);
      setError(err.message || 'Failed to remove assignment');
    } finally {
      setIsRemoving(null);
    }
  };

  if (!isOpen) return null;

  return (
    <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
      <div className="bg-white rounded-lg shadow-xl max-w-2xl w-full mx-4 max-h-[80vh] overflow-hidden">
        {/* Header */}
        <div className="flex items-center justify-between p-6 border-b border-gray-200">
          <div>
            <h2 className="text-xl font-semibold text-gray-900">
              Elderly Assigned to {caregiverName}
            </h2>
            <p className="text-sm text-gray-600 mt-1">
              {elderly.length} elderly {elderly.length === 1 ? 'person' : 'people'} assigned
            </p>
          </div>
          <button
            onClick={handleClose}
            className="text-gray-400 hover:text-gray-600 transition-colors"
          >
            <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
            </svg>
          </button>
        </div>

        {/* Content */}
        <div className="p-6 overflow-y-auto max-h-[60vh]">
          {loading ? (
            <div className="flex items-center justify-center py-8">
              <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-600"></div>
              <span className="ml-3 text-gray-600">Loading assignments...</span>
            </div>
          ) : error ? (
            <div className="text-center py-8">
              <div className="text-red-600 mb-2">
                <svg className="w-12 h-12 mx-auto mb-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-2.5L13.732 4c-.77-.833-1.964-.833-2.732 0L3.732 16.5c-.77.833.192 2.5 1.732 2.5z" />
                </svg>
              </div>
              <p className="text-red-600 font-medium">{error}</p>
              <button
                onClick={fetchElderlyForCaregiver}
                className="mt-4 px-4 py-2 bg-red-600 text-white rounded-lg hover:bg-red-700 transition-colors"
              >
                Try Again
              </button>
            </div>
          ) : elderly.length === 0 ? (
            <div className="text-center py-8">
              <div className="text-gray-400 mb-4">
                <svg className="w-12 h-12 mx-auto mb-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M17 20h5v-2a3 3 0 00-5.356-1.857M17 20H7m10 0v-2c0-.656-.126-1.283-.356-1.857M7 20H2v-2a3 3 0 015.356-1.857M7 20v-2c0-.656.126-1.283.356-1.857m0 0a5.002 5.002 0 019.288 0M15 7a3 3 0 11-6 0 3 3 0 016 0zm6 3a2 2 0 11-4 0 2 2 0 014 0zM7 10a2 2 0 11-4 0 2 2 0 014 0z" />
                </svg>
              </div>
              <p className="text-gray-600 font-medium">No elderly assigned</p>
              <p className="text-gray-500 text-sm mt-1">
                This caregiver doesn't have any elderly people assigned yet.
              </p>
            </div>
          ) : (
            <div className="space-y-4">
              {elderly.map((person) => (
                <div
                  key={person.id}
                  className="bg-gray-50 rounded-lg p-4 border border-gray-200 hover:bg-gray-100 transition-colors"
                >
                  <div className="flex items-center justify-between">
                    <div className="flex items-center space-x-3">
                      {/* Avatar */}
                      <div className="w-10 h-10 bg-purple-100 rounded-full flex items-center justify-center">
                        <span className="text-purple-600 font-semibold text-sm">
                          {person.name.split(' ').map(n => n[0]).join('').toUpperCase()}
                        </span>
                      </div>
                      
                      {/* Info */}
                      <div>
                        <h3 className="font-medium text-gray-900">{person.name}</h3>
                        <p className="text-sm text-gray-600">ID: {person.custom_id}</p>
                      </div>
                    </div>
                    
                    {/* Status indicators and delete button */}
                    <div className="flex items-center space-x-2">
                      {person.tasks && person.tasks.length > 0 && (
                        <span className="inline-flex items-center px-2 py-1 rounded-full text-xs font-medium bg-blue-100 text-blue-800">
                          {person.tasks.length} task{person.tasks.length !== 1 ? 's' : ''}
                        </span>
                      )}
                      {person.medications && person.medications.length > 0 && (
                        <span className="inline-flex items-center px-2 py-1 rounded-full text-xs font-medium bg-green-100 text-green-800">
                          {person.medications.length} medication{person.medications.length !== 1 ? 's' : ''}
                        </span>
                      )}
                      <button
                        onClick={() => handleRemoveAssignment(person.id)}
                        disabled={isRemoving === person.id}
                        className="p-2 text-red-600 hover:bg-red-100 rounded-md border border-gray-300 hover:border-red-300 disabled:opacity-50 disabled:cursor-not-allowed"
                        title="Remove assignment"
                      >
                        {isRemoving === person.id ? (
                          <svg className="w-4 h-4 animate-spin" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15" />
                          </svg>
                        ) : (
                          <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16" />
                          </svg>
                        )}
                      </button>
                    </div>
                  </div>
                </div>
              ))}
            </div>
          )}
        </div>

        {/* Footer */}
        <div className="flex items-center justify-end p-6 border-t border-gray-200 bg-gray-50">
          <button
            onClick={handleClose}
            className="px-4 py-2 bg-gray-600 text-white rounded-lg hover:bg-gray-700 transition-colors"
          >
            Close
          </button>
        </div>
      </div>
    </div>
  );
};

export default AssignmentModal;
