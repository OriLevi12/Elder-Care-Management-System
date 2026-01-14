import React from 'react';
import CaregiverCard from '../cards/CaregiverCard';

/**
 * Table component for displaying caregivers data
 */
const CaregiverTable = ({ caregivers, onDelete, onGeneratePDF, onUpdateSalary, onAssignmentChanged }) => {
  return (
    <div className="bg-white rounded-xl shadow-lg overflow-hidden">
      <div className="px-6 py-4 bg-gray-50 border-b border-gray-200">
        <h2 className="text-xl font-semibold text-gray-800">Professional Caregivers</h2>
      </div>
      
      <div className="overflow-x-auto">
        <table className="w-full">
          <thead className="bg-gray-50">
            <tr>
              <th className="px-6 py-4 text-left text-sm font-medium text-gray-700">Name</th>
              <th className="px-6 py-4 text-left text-sm font-medium text-gray-700">ID</th>
              <th className="px-6 py-4 text-left text-sm font-medium text-gray-700">Base Salary</th>
              <th className="px-6 py-4 text-left text-sm font-medium text-gray-700">Total Allowance</th>
              <th className="px-6 py-4 text-left text-sm font-medium text-gray-700">Total Saturday Pay</th>
              <th className="px-6 py-4 text-left text-sm font-medium text-gray-700">Total Salary</th>
              <th className="px-6 py-4 text-left text-sm font-medium text-gray-700">Assigned Elderly</th>
              <th className="px-6 py-4 text-left text-sm font-medium text-gray-700">Actions</th>
            </tr>
          </thead>
          <tbody className="divide-y divide-gray-200">
            {caregivers.map((caregiver) => (
              <CaregiverCard key={caregiver.id} caregiver={caregiver} onDelete={onDelete} onGeneratePDF={onGeneratePDF} onUpdateSalary={onUpdateSalary} onAssignmentChanged={onAssignmentChanged} />
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
};

export default CaregiverTable;
