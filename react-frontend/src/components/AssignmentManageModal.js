import React, { useState, useEffect } from 'react';
import assignmentService from '../services/assignmentService';

const AssignmentManageModal = ({ isOpen, onClose, caregiverId, caregiverName, onAssignmentChanged }) => {
  const [assignedElderly, setAssignedElderly] = useState([]);
  const [allElderly, setAllElderly] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [selectedElderlyId, setSelectedElderlyId] = useState('');
  const [isAssigning, setIsAssigning] = useState(false);
  const [isRemoving, setIsRemoving] = useState(null);

  useEffect(() => {
    if (isOpen && caregiverId) {
      fetchData();
    }
  }, [isOpen, caregiverId]);

  const fetchData = async () => {
    setLoading(true);
    setError(null);
    
    try {
      // Fetch both assigned elderly and all elderly with assignment status
      const [assigned, allElderlyWithStatus] = await Promise.all([
        assignmentService.getElderlyForCaregiver(caregiverId),
        assignmentService.getAllElderlyForAssignment(caregiverId)
      ]);
      
      setAssignedElderly(assigned);
      setAllElderly(allElderlyWithStatus);
    } catch (err) {
      console.error('Error fetching assignment data:', err);
      setError(err.message || 'Failed to load assignment data');
    } finally {
      setLoading(false);
    }
  };

  const handleAssignElderly = async () => {
    if (!selectedElderlyId) return;
    
    setIsAssigning(true);
    try {
      await assignmentService.createAssignment(caregiverId, parseInt(selectedElderlyId));
      
      // Refresh data
      await fetchData();
      
      // Notify parent component
      if (onAssignmentChanged) {
        onAssignmentChanged();
      }
      
      // Reset selection
      setSelectedElderlyId('');
    } catch (err) {
      console.error('Error assigning elderly:', err);
      setError(err.message || 'Failed to assign elderly');
    } finally {
      setIsAssigning(false);
    }
  };

  const handleRemoveAssignment = async (elderlyId) => {
    setIsRemoving(elderlyId);
    try {
      await assignmentService.deleteAssignment(caregiverId, elderlyId);
      
      // Refresh data
      await fetchData();
      
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

  const handleClose = () => {
    setAssignedElderly([]);
    setAllElderly([]);
    setError(null);
    setSelectedElderlyId('');
    onClose();
  };

  if (!isOpen) return null;

  return (
    <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
      <div className="bg-white rounded-lg shadow-xl max-w-4xl w-full mx-4 max-h-[90vh] overflow-hidden">
        {/* Header */}
        <div className="flex items-center justify-between p-6 border-b border-gray-200">
          <div>
            <h2 className="text-xl font-semibold text-gray-900">
              Manage Assignments for {caregiverName}
            </h2>
            <p className="text-sm text-gray-600 mt-1">
              Add or remove elderly assignments
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
        <div className="p-6 overflow-y-auto max-h-[70vh]">
          {loading ? (
            <div className="flex items-center justify-center py-8">
              <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-purple-600"></div>
              <span className="ml-3 text-gray-600">Loading assignment data...</span>
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
                onClick={fetchData}
                className="mt-4 px-4 py-2 bg-red-600 text-white rounded-lg hover:bg-red-700 transition-colors"
              >
                Try Again
              </button>
            </div>
          ) : (
            <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
              {/* Currently Assigned */}
              <div>
                <h3 className="text-lg font-medium text-gray-900 mb-4">
                  Currently Assigned ({assignedElderly.length})
                </h3>
                {assignedElderly.length === 0 ? (
                  <div className="text-center py-8 bg-gray-50 rounded-lg">
                    <div className="text-gray-400 mb-2">
                      <svg className="w-8 h-8 mx-auto mb-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M17 20h5v-2a3 3 0 00-5.356-1.857M17 20H7m10 0v-2c0-.656-.126-1.283-.356-1.857M7 20H2v-2a3 3 0 015.356-1.857M7 20v-2c0-.656.126-1.283.356-1.857m0 0a5.002 5.002 0 019.288 0M15 7a3 3 0 11-6 0 3 3 0 016 0zm6 3a2 2 0 11-4 0 2 2 0 014 0zM7 10a2 2 0 11-4 0 2 2 0 014 0z" />
                      </svg>
                    </div>
                    <p className="text-gray-600 text-sm">No elderly assigned</p>
                  </div>
                ) : (
                  <div className="space-y-3">
                    {assignedElderly.map((person) => (
                      <div
                        key={person.id}
                        className="bg-green-50 border border-green-200 rounded-lg p-4 flex items-center justify-between"
                      >
                        <div className="flex items-center space-x-3">
                          <div className="w-8 h-8 bg-green-100 rounded-full flex items-center justify-center">
                            <span className="text-green-600 font-semibold text-xs">
                              {person.name.split(' ').map(n => n[0]).join('').toUpperCase()}
                            </span>
                          </div>
                          <div>
                            <h4 className="font-medium text-gray-900">{person.name}</h4>
                            <p className="text-sm text-gray-600">ID: {person.custom_id}</p>
                          </div>
                        </div>
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
                    ))}
                  </div>
                )}
              </div>

              {/* Add New Assignment */}
              <div>
                <h3 className="text-lg font-medium text-gray-900 mb-4">
                  Add New Assignment
                </h3>
                {allElderly.length === 0 ? (
                  <div className="text-center py-8 bg-gray-50 rounded-lg">
                    <div className="text-gray-400 mb-2">
                      <svg className="w-8 h-8 mx-auto mb-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M17 20h5v-2a3 3 0 00-5.356-1.857M17 20H7m10 0v-2c0-.656-.126-1.283-.356-1.857M7 20H2v-2a3 3 0 015.356-1.857M7 20v-2c0-.656.126-1.283.356-1.857m0 0a5.002 5.002 0 019.288 0M15 7a3 3 0 11-6 0 3 3 0 016 0zm6 3a2 2 0 11-4 0 2 2 0 014 0zM7 10a2 2 0 11-4 0 2 2 0 014 0z" />
                      </svg>
                    </div>
                    <p className="text-gray-600 text-sm">No elderly available</p>
                  </div>
                ) : (
                  <div className="space-y-4">
                    <div>
                      <label className="block text-sm font-medium text-gray-700 mb-2">
                        Select Elderly to Assign
                      </label>
                      <select
                        value={selectedElderlyId}
                        onChange={(e) => setSelectedElderlyId(e.target.value)}
                        className="w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-purple-500 focus:border-purple-500"
                      >
                        <option value="">Choose an elderly person...</option>
                        {allElderly.map((person) => (
                          <option 
                            key={person.id} 
                            value={person.id}
                            disabled={person.isAssignedToThisCaregiver}
                          >
                            {person.name} (ID: {person.custom_id})
                            {person.isAssignedToThisCaregiver ? ' - Already assigned' : ''}
                          </option>
                        ))}
                      </select>
                    </div>
                    <button
                      onClick={handleAssignElderly}
                      disabled={!selectedElderlyId || isAssigning || allElderly.find(p => p.id === parseInt(selectedElderlyId))?.isAssignedToThisCaregiver}
                      className="w-full px-4 py-2 bg-purple-600 text-white rounded-lg hover:bg-purple-700 disabled:opacity-50 disabled:cursor-not-allowed transition-colors flex items-center justify-center"
                    >
                      {isAssigning ? (
                        <>
                          <svg className="w-4 h-4 mr-2 animate-spin" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15" />
                          </svg>
                          Assigning...
                        </>
                      ) : (
                        <>
                          <svg className="w-4 h-4 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 6v6m0 0v6m0-6h6m-6 0H6" />
                          </svg>
                          Assign Elderly
                        </>
                      )}
                    </button>
                  </div>
                )}
              </div>
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

export default AssignmentManageModal;
