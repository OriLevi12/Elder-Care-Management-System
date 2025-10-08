import React, { useState } from 'react';
import { formatCurrency, getInitials } from '../utils/formatters';
import UpdateSalaryModal from './UpdateSalaryModal';
import AssignmentModal from './AssignmentModal';
import AssignmentManageModal from './AssignmentManageModal';

/**
 * Individual caregiver row component
 * Updated to work with backend data structure
 */
const CaregiverCard = ({ caregiver, onDelete, onGeneratePDF, onUpdateSalary, onAssignmentChanged }) => {
  const [showDeleteModal, setShowDeleteModal] = useState(false);
  const [isGeneratingPDF, setIsGeneratingPDF] = useState(false);
  const [showUpdateSalaryModal, setShowUpdateSalaryModal] = useState(false);
  const [showAssignmentModal, setShowAssignmentModal] = useState(false);
  const [showManageModal, setShowManageModal] = useState(false);
  
  // Map backend data structure to display format
  const baseSalary = caregiver.salary?.price || 0;
  const totalAllowance = caregiver.allowance?.price || 0;
  const totalSaturdayPay = caregiver.saturday?.price || 0;
  const totalSalary = baseSalary + totalAllowance + totalSaturdayPay;
  const assignedElderly = caregiver.assignments?.length || 0;

  const handleDeleteClick = () => {
    setShowDeleteModal(true);
  };

  const handleConfirmDelete = () => {
    onDelete(caregiver.id);
    setShowDeleteModal(false);
  };

  const handleCancelDelete = () => {
    setShowDeleteModal(false);
  };

  const handleGeneratePDF = async () => {
    setIsGeneratingPDF(true);
    try {
      await onGeneratePDF(caregiver.id);
    } catch (error) {
      console.error('Error generating PDF:', error);
    } finally {
      setIsGeneratingPDF(false);
    }
  };

  const handleUpdateSalaryClick = () => {
    setShowUpdateSalaryModal(true);
  };

  const handleCloseUpdateSalaryModal = () => {
    setShowUpdateSalaryModal(false);
  };

  const handleViewAssignments = () => {
    setShowAssignmentModal(true);
  };

  const handleCloseAssignmentModal = () => {
    setShowAssignmentModal(false);
  };

  const handleManageAssignments = () => {
    setShowManageModal(true);
  };

  const handleCloseManageModal = () => {
    setShowManageModal(false);
  };

  const handleAssignmentChanged = () => {
    if (onAssignmentChanged) {
      onAssignmentChanged();
    }
  };

  return (
    <>
      <tr className="hover:bg-gray-50">
      {/* Name Column */}
      <td className="px-6 py-4">
        <div className="flex items-center">
          <div className="w-10 h-10 bg-purple-500 rounded-full flex items-center justify-center mr-3">
            <span className="text-white text-sm font-semibold">
              {getInitials(caregiver.name)}
            </span>
          </div>
          <div>
            <div className="text-sm font-medium text-gray-900">{caregiver.name}</div>
            <div className="text-sm text-gray-500">Professional Caregiver</div>
          </div>
        </div>
      </td>
      
      {/* ID Column */}
      <td className="px-6 py-4">
        <span className="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-blue-100 text-blue-800">
          {caregiver.custom_id || caregiver.id}
        </span>
      </td>
      
      {/* Base Salary Column */}
      <td className="px-6 py-4">
        <span className="text-sm text-green-600 font-medium">
          {formatCurrency(baseSalary)}
        </span>
      </td>
      
      {/* Total Allowance Column */}
      <td className="px-6 py-4">
        <span className="text-sm text-orange-600 font-medium">
          {formatCurrency(totalAllowance)}
        </span>
      </td>
      
      {/* Total Saturday Pay Column */}
      <td className="px-6 py-4">
        <span className="text-sm text-purple-600 font-medium">
          {formatCurrency(totalSaturdayPay)}
        </span>
      </td>
      
      {/* Total Salary Column */}
      <td className="px-6 py-4">
        <span className="inline-flex items-center px-3 py-1 rounded-full text-sm font-medium bg-green-100 text-green-800">
          {formatCurrency(totalSalary)}
        </span>
      </td>
      
      {/* Assigned Elderly Column */}
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
            View ({assignedElderly})
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
      
      {/* Actions Column */}
      <td className="px-6 py-4">
        <div className="flex space-x-2">
          <button 
            onClick={handleGeneratePDF}
            disabled={isGeneratingPDF}
            className="p-2 text-blue-600 hover:bg-blue-100 rounded-md border border-gray-300 hover:border-blue-300 disabled:opacity-50 disabled:cursor-not-allowed"
            title={isGeneratingPDF ? "Generating PDF..." : "Generate PDF Report"}
          >
            {isGeneratingPDF ? (
              <svg className="w-4 h-4 animate-spin" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15" />
              </svg>
            ) : (
              <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
              </svg>
            )}
          </button>
          <button 
            onClick={handleUpdateSalaryClick}
            className="p-2 text-green-600 hover:bg-green-100 rounded-md border border-gray-300 hover:border-green-300"
            title="Update salary"
          >
            <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z" />
            </svg>
          </button>
          <button 
            onClick={handleDeleteClick}
            className="p-2 text-red-600 hover:bg-red-100 rounded-md border border-gray-300 hover:border-red-300"
            title="Delete caregiver"
          >
            <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16" />
            </svg>
          </button>
        </div>
      </td>
    </tr>
    {/* Delete Confirmation Modal */}
    {showDeleteModal && (
      <div className="fixed inset-0 bg-gray-600 bg-opacity-50 overflow-y-auto h-full w-full z-50 flex justify-center items-center">
        <div className="relative p-6 bg-white w-full max-w-md mx-auto rounded-lg shadow-lg">
          <div className="flex items-center mb-4">
            <div className="mx-auto flex-shrink-0 flex items-center justify-center h-12 w-12 rounded-full bg-red-100">
              <svg className="h-6 w-6 text-red-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-2.5L13.732 4c-.77-.833-1.964-.833-2.732 0L3.732 16.5c-.77.833.192 2.5 1.732 2.5z" />
              </svg>
            </div>
          </div>
          <div className="text-center">
            <h3 className="text-lg font-medium text-gray-900 mb-2">
              Delete Caregiver
            </h3>
            <p className="text-sm text-gray-500 mb-6">
              Are you sure you want to delete caregiver <strong>{caregiver.name}</strong>? This action cannot be undone.
            </p>
            <div className="flex justify-center space-x-3">
              <button
                onClick={handleCancelDelete}
                className="px-4 py-2 border border-gray-300 rounded-md shadow-sm text-sm font-medium text-gray-700 hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500"
              >
                Cancel
              </button>
              <button
                onClick={handleConfirmDelete}
                className="px-4 py-2 bg-red-600 border border-transparent rounded-md shadow-sm text-sm font-medium text-white hover:bg-red-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-red-500"
              >
                Delete
              </button>
            </div>
          </div>
        </div>
      </div>
    )}
    
    {/* Update Salary Modal */}
    {showUpdateSalaryModal && (
      <UpdateSalaryModal
        caregiver={caregiver}
        isOpen={showUpdateSalaryModal}
        onClose={handleCloseUpdateSalaryModal}
        onSalaryUpdated={onUpdateSalary}
      />
    )}
    
    {/* Assignment Modal */}
    {showAssignmentModal && (
      <AssignmentModal
        isOpen={showAssignmentModal}
        onClose={handleCloseAssignmentModal}
        caregiverId={caregiver.id}
        caregiverName={caregiver.name}
        onAssignmentChanged={handleAssignmentChanged}
      />
    )}
    
    {/* Assignment Manage Modal */}
    {showManageModal && (
      <AssignmentManageModal
        isOpen={showManageModal}
        onClose={handleCloseManageModal}
        caregiverId={caregiver.id}
        caregiverName={caregiver.name}
        onAssignmentChanged={handleAssignmentChanged}
      />
    )}
    </>
  );
};

export default CaregiverCard;
