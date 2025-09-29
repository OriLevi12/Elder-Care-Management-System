import React from 'react';
import DashboardHeader from './DashboardHeader';
import CaregiverTable from './CaregiverTable';
import { sampleCaregivers } from '../data/sampleCaregivers';

/**
 * Main Caregivers Dashboard component
 * Now much cleaner and more maintainable with separated concerns
 */
function CaregiversDashboard() {
  return (
    <div className="container mx-auto p-6 max-w-6xl">
      <DashboardHeader />
      <CaregiverTable caregivers={sampleCaregivers} />
    </div>
  );
}

export default CaregiversDashboard;
