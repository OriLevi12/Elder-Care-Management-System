import React from 'react';
import { formatCurrency, getInitials } from '../utils/formatters';

/**
 * Individual caregiver row component
 * Updated to work with backend data structure
 */
const CaregiverCard = ({ caregiver }) => {
  // Map backend data structure to display format
  const baseSalary = caregiver.salary?.price || 0;
  const totalAllowance = caregiver.allowance?.price || 0;
  const totalSaturdayPay = caregiver.saturday?.price || 0;
  const totalSalary = baseSalary + totalAllowance + totalSaturdayPay;
  const assignedElderly = caregiver.assignments?.length || 0;

  return (
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
        <button className="inline-flex items-center px-3 py-1 border border-transparent text-sm font-medium rounded-md text-blue-700 bg-blue-100 hover:bg-blue-200 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500">
          <svg className="w-4 h-4 mr-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15 12a3 3 0 11-6 0 3 3 0 016 0z" />
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M2.458 12C3.732 7.943 7.523 5 12 5c4.478 0 8.268 2.943 9.542 7-1.274 4.057-5.064 7-9.542 7-4.477 0-8.268-2.943-9.542-7z" />
          </svg>
          View ({assignedElderly})
        </button>
      </td>
      
      {/* Actions Column */}
      <td className="px-6 py-4">
        <div className="flex space-x-2">
          <button className="p-2 text-blue-600 hover:bg-blue-100 rounded-md border border-gray-300 hover:border-blue-300">
            <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
            </svg>
          </button>
          <button className="p-2 text-green-600 hover:bg-green-100 rounded-md border border-gray-300 hover:border-green-300">
            <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z" />
            </svg>
          </button>
          <button className="p-2 text-red-600 hover:bg-red-100 rounded-md border border-gray-300 hover:border-red-300">
            <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16" />
            </svg>
          </button>
        </div>
      </td>
    </tr>
  );
};

export default CaregiverCard;
