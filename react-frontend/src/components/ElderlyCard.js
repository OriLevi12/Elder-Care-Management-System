import React, { useState } from 'react';
import { getInitials } from '../utils/formatters';
import AssignmentModal from './AssignmentModal';
import AssignmentManageModal from './AssignmentManageModal';
import AssignCaregiverModal from './AssignCaregiverModal';
import DeleteElderlyModal from './DeleteElderlyModal';
import AddTaskModal from './AddTaskModal';
import ViewTasksModal from './ViewTasksModal';
import AddMedicationModal from './AddMedicationModal';
import ViewMedicationsModal from './ViewMedicationsModal';
import ViewCaregiversModal from './ViewCaregiversModal';

/**
 * Individual elderly row component
 * Updated to work with backend data structure
 */
const ElderlyCard = ({ elderly, onDelete, onTaskAdded, onMedicationAdded }) => {
  const [showDeleteModal, setShowDeleteModal] = useState(false);
  const [showManageModal, setShowManageModal] = useState(false);
  const [showTaskModal, setShowTaskModal] = useState(false);
  const [showViewTasksModal, setShowViewTasksModal] = useState(false);
  const [showMedicationModal, setShowMedicationModal] = useState(false);
  const [showViewMedicationsModal, setShowViewMedicationsModal] = useState(false);
  const [showViewCaregiversModal, setShowViewCaregiversModal] = useState(false);
  
  // Map backend data structure to display format
  const assignedCaregivers = elderly.assignments?.length || 0;
  const tasksCount = elderly.tasks?.length || 0;
  const medicationsCount = elderly.medications?.length || 0;

  const handleDeleteClick = () => {
    setShowDeleteModal(true);
  };

  const handleConfirmDelete = () => {
    onDelete(elderly.id);
    setShowDeleteModal(false);
  };

  const handleCancelDelete = () => {
    setShowDeleteModal(false);
  };

  const handleViewAssignments = () => {
    setShowViewCaregiversModal(true);
  };


  const handleManageAssignments = () => {
    setShowManageModal(true);
  };

  const handleCloseManageModal = () => {
    setShowManageModal(false);
  };

  const handleAssignmentChanged = () => {
    // This will trigger a refresh in the parent component
    if (onTaskAdded) {
      onTaskAdded(); // Reuse the refresh callback
    }
  };

  const handleAddTask = () => {
    setShowTaskModal(true);
  };

  const handleCloseTaskModal = () => {
    setShowTaskModal(false);
  };

  const handleTaskAdded = () => {
    if (onTaskAdded) {
      onTaskAdded();
    }
    setShowTaskModal(false);
  };

  const handleViewTasks = () => {
    setShowViewTasksModal(true);
  };

  const handleCloseViewTasksModal = () => {
    setShowViewTasksModal(false);
  };

  const handleAddMedication = () => {
    setShowMedicationModal(true);
  };

  const handleCloseMedicationModal = () => {
    setShowMedicationModal(false);
  };

  const handleMedicationAdded = () => {
    if (onMedicationAdded) {
      onMedicationAdded();
    }
    setShowMedicationModal(false);
  };

  const handleViewMedications = () => {
    setShowViewMedicationsModal(true);
  };

  const handleCloseViewMedicationsModal = () => {
    setShowViewMedicationsModal(false);
  };

  return (
    <>
      <tr className="hover:bg-gray-50">
      {/* Name Column */}
      <td className="px-6 py-4">
        <div className="flex items-center">
          <div className="w-10 h-10 bg-blue-500 rounded-full flex items-center justify-center mr-3">
            <span className="text-white text-sm font-semibold">
              {getInitials(elderly.name)}
            </span>
          </div>
          <div>
            <div className="text-sm font-medium text-gray-900">{elderly.name}</div>
            <div className="text-sm text-gray-500">Elderly Client</div>
          </div>
        </div>
      </td>
      
      {/* ID Column */}
      <td className="px-6 py-4">
        <span className="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-blue-100 text-blue-800">
          {elderly.custom_id || elderly.id}
        </span>
      </td>
      
      {/* Assigned Caregivers Column */}
      <td className="px-6 py-4">
        <div className="flex space-x-2">
          <button 
            onClick={handleViewAssignments}
            className="inline-flex items-center px-3 py-1 border border-transparent text-sm font-medium rounded-md text-blue-700 bg-blue-100 hover:bg-blue-200 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500 transition-colors"
          >
            <svg className="w-4 h-4 mr-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15 12a3 3 0 11-6 0 3 3 0 016 0z" />
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M2.458 12C3.732 7.943 7.523 5 12 5c4.478 0 8.268 2.943 9.542 7-1.274 4.057-5.064 7-9.542 7-4.477 0-8.268-2.943-9.542-7z" />
            </svg>
            View ({assignedCaregivers})
          </button>
          <button 
            onClick={handleManageAssignments}
            className="inline-flex items-center px-3 py-1 border border-transparent text-sm font-medium rounded-md text-purple-700 bg-purple-100 hover:bg-purple-200 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-purple-500 transition-colors"
            title="Manage assignments"
          >
            <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 6v6m0 0v6m0-6h6m-6 0H6" />
            </svg>
          </button>
        </div>
      </td>
      
      {/* Tasks Column */}
      <td className="px-6 py-4">
        <div className="flex items-center space-x-2">
          <button 
            onClick={handleViewTasks}
            className="inline-flex items-center px-3 py-1 border border-transparent text-sm font-medium rounded-md text-orange-700 bg-orange-100 hover:bg-orange-200 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-orange-500 transition-colors"
          >
            <svg className="w-4 h-4 mr-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15 12a3 3 0 11-6 0 3 3 0 016 0z" />
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M2.458 12C3.732 7.943 7.523 5 12 5c4.478 0 8.268 2.943 9.542 7-1.274 4.057-5.064 7-9.542 7-4.477 0-8.268-2.943-9.542-7z" />
            </svg>
            View ({tasksCount})
          </button>
          <button 
            onClick={handleAddTask}
            className="inline-flex items-center px-2 py-1 border border-transparent text-sm font-medium rounded-md text-orange-700 bg-orange-100 hover:bg-orange-200 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-orange-500 transition-colors"
            title="Add task"
          >
            <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 4v16m8-8H4" />
            </svg>
          </button>
        </div>
      </td>
      
      {/* Medications Column */}
      <td className="px-6 py-4">
        <div className="flex items-center space-x-2">
          <button 
            onClick={handleViewMedications}
            className="inline-flex items-center px-3 py-1 border border-transparent text-sm font-medium rounded-md text-green-700 bg-green-100 hover:bg-green-200 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-green-500 transition-colors"
          >
            <svg className="w-4 h-4 mr-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15 12a3 3 0 11-6 0 3 3 0 016 0z" />
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M2.458 12C3.732 7.943 7.523 5 12 5c4.478 0 8.268 2.943 9.542 7-1.274 4.057-5.064 7-9.542 7-4.477 0-8.268-2.943-9.542-7z" />
            </svg>
            View ({medicationsCount})
          </button>
          <button 
            onClick={handleAddMedication}
            className="inline-flex items-center px-2 py-1 border border-transparent text-sm font-medium rounded-md text-green-700 bg-green-100 hover:bg-green-200 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-green-500 transition-colors"
            title="Add medication"
          >
            <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 4v16m8-8H4" />
            </svg>
          </button>
        </div>
      </td>
      
      {/* Actions Column */}
      <td className="px-6 py-4">
        <div className="flex space-x-2">
          <button 
            onClick={handleDeleteClick}
            className="p-2 text-red-600 hover:bg-red-100 rounded-md border border-gray-300 hover:border-red-300"
            title="Delete elderly"
          >
            <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16" />
            </svg>
          </button>
        </div>
      </td>
    </tr>
    
    {/* Delete Confirmation Modal */}
    <DeleteElderlyModal
      isOpen={showDeleteModal}
      onClose={handleCancelDelete}
      onConfirm={handleConfirmDelete}
      elderlyName={elderly.name}
    />
    
    {/* View Caregivers Modal */}
    <ViewCaregiversModal
      isOpen={showViewCaregiversModal}
      onClose={() => setShowViewCaregiversModal(false)}
      elderlyId={elderly.id}
      elderlyName={elderly.name}
    />
    
    {/* Assign Caregiver Modal */}
    <AssignCaregiverModal
      isOpen={showManageModal}
      onClose={handleCloseManageModal}
      elderlyId={elderly.id}
      elderlyName={elderly.name}
      onAssignmentChanged={handleAssignmentChanged}
    />
    
    {/* Add Task Modal */}
    <AddTaskModal
      isOpen={showTaskModal}
      onClose={handleCloseTaskModal}
      onTaskAdded={handleTaskAdded}
      elderlyId={elderly.id}
      elderlyName={elderly.name}
    />
    
    {/* View Tasks Modal */}
    <ViewTasksModal
      isOpen={showViewTasksModal}
      onClose={handleCloseViewTasksModal}
      elderlyId={elderly.id}
      elderlyName={elderly.name}
      tasks={elderly.tasks}
    />
    
    {/* Add Medication Modal */}
    <AddMedicationModal
      isOpen={showMedicationModal}
      onClose={handleCloseMedicationModal}
      onMedicationAdded={handleMedicationAdded}
      elderlyId={elderly.id}
      elderlyName={elderly.name}
    />
    
    {/* View Medications Modal */}
    <ViewMedicationsModal
      isOpen={showViewMedicationsModal}
      onClose={handleCloseViewMedicationsModal}
      elderlyId={elderly.id}
      elderlyName={elderly.name}
      medications={elderly.medications}
    />
    </>
  );
};

export default ElderlyCard;
