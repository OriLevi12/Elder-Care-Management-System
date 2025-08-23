import React from 'react';

function CaregiversDashboard() {
  return (
    <div className="container mx-auto p-6 max-w-6xl">
      {/* Gradient Banner */}
      <div className="bg-gradient-to-r from-blue-500 via-purple-600 to-pink-500 rounded-xl p-8 mb-8 shadow-lg">
        {/* Icons Row */}
        <div className="flex gap-2 mb-6">
          {/* People Icon */}
          <div className="w-12 h-12 bg-white/20 rounded-lg flex items-center justify-center backdrop-blur-sm">
            <svg className="w-6 h-6 text-white" fill="orange" stroke="yellow" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M17 20h5v-2a3 3 0 00-5.356-1.857M17 20H7m10 0v-2c0-.656-.126-1.283-.356-1.857M7 20H2v-2a3 3 0 015.356-1.857M7 20v-2c0-.656.126-1.283.356-1.857m0 0a5.002 5.002 0 019.288 0M15 7a3 3 0 11-6 0 3 3 0 016 0zm6 3a2 2 0 11-4 0 2 2 0 014 0zM7 10a2 2 0 11-4 0 2 2 0 014 0z" />
            </svg>
          </div>
          
          {/* Heart Icon */}
          <div className="w-12 h-12 bg-white/20 rounded-lg flex items-center justify-center backdrop-blur-sm">
            <svg className="w-6 h-6 text-white" fill="red" stroke="red" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4.318 6.318a4.5 4.5 0 000 6.364L12 20.364l7.682-7.682a4.5 4.5 0 00-6.364-6.364L12 7.636l-1.318-1.318a4.5 4.5 0 00-6.364 0z" />
            </svg>
          </div>
          
          {/* Shield Icon */}
          <div className="w-12 h-12 bg-white/20 rounded-lg flex items-center justify-center backdrop-blur-sm">
            <svg className="w-6 h-6 text-yellow" fill="blue" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12l2 2 4-4m5.618-4.016A11.955 11.955 0 0112 2.944a11.955 11.955 0 01-8.618 3.04A12.02 12.02 0 003 9c0 5.591 3.824 10.29 9 11.622 5.176-1.332 9-6.03 9-11.622 0-1.042-.133-2.052-.382-3.016z" />
            </svg>
          </div>
        </div>
        
        {/* Title and Subtitle */}
        <h1 className="text-4xl font-bold text-white mb-2">Caregiver Dashboard</h1>
        <p className="text-white/90 text-lg">Manage your caregiver database with comprehensive information and banking details.</p>
      </div>
    
    </div>
  );
}

export default CaregiversDashboard;
