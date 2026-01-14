import React from 'react';
import ElderlyCard from '../cards/ElderlyCard';

/**
 * Table component for displaying elderly data
 */
const ElderlyTable = ({ elderly, onDelete, onTaskAdded, onMedicationAdded }) => {
  return (
    <div className="bg-white rounded-xl shadow-lg overflow-hidden">
      <div className="px-6 py-4 bg-gray-50 border-b border-gray-200">
        <h2 className="text-xl font-semibold text-gray-800">Elderly Clients</h2>
      </div>
      
      <div className="overflow-x-auto">
        <table className="w-full">
          <thead className="bg-gray-50">
            <tr>
              <th className="px-6 py-4 text-left text-sm font-medium text-gray-700">Name</th>
              <th className="px-6 py-4 text-left text-sm font-medium text-gray-700">ID</th>
              <th className="px-6 py-4 text-left text-sm font-medium text-gray-700">Assigned Caregivers</th>
              <th className="px-6 py-4 text-left text-sm font-medium text-gray-700">Tasks</th>
              <th className="px-6 py-4 text-left text-sm font-medium text-gray-700">Medications</th>
              <th className="px-6 py-4 text-left text-sm font-medium text-gray-700">Actions</th>
            </tr>
          </thead>
          <tbody className="divide-y divide-gray-200">
            {elderly.map((elderlyPerson) => (
              <ElderlyCard 
                key={elderlyPerson.id} 
                elderly={elderlyPerson} 
                onDelete={onDelete}
                onTaskAdded={onTaskAdded}
                onMedicationAdded={onMedicationAdded}
              />
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
};

export default ElderlyTable;
