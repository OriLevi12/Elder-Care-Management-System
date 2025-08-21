import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';

function Header() {
  const [isMobileMenuOpen, setIsMobileMenuOpen] = useState(false);
  const navigate = useNavigate();
  
  const toggleMobileMenu = () => {
    setIsMobileMenuOpen(!isMobileMenuOpen);
  };

  return (
    <header className="bg-blue-600 text-white shadow-lg">
      <div className="container mx-auto px-6 py-4">
        <div className="flex items-center justify-between">
          {/* Logo and Title */}
          <div className="flex items-center space-x-3">
            <div className="w-10 h-10 bg-white rounded-full flex items-center justify-center">
              <span className="text-blue-600 font-bold text-xl">❤️</span>
            </div>
            <h1
              onClick={() => navigate('/')}
              className="text-2xl font-bold cursor-pointer hover:text-blue-200"
            >
              Elder Care Manager
            </h1>
          </div>

          {/* Desktop Navigation - Hidden on Mobile */}
          <nav className="hidden md:flex space-x-6">
            <a href="/caregiver-dashboard" className="hover:text-blue-200 transition-colors">Caregiver Dashboard</a>
            <a href="/elder-dashboard" className="hover:text-blue-200 transition-colors">Elder Dashboard</a>
            <a href="/manage-caregivers" className="hover:text-blue-200 transition-colors">Manage Caregivers</a>
            <a href="/manage-elderly" className="hover:text-blue-200 transition-colors">Manage Elderly</a>
          </nav>

          {/* Right Side */}
          <div className="flex items-center space-x-4">
            {/* Mobile Menu Button - Only Visible on Mobile */}
            <button 
              onClick={toggleMobileMenu}
              className="md:hidden bg-blue-700 hover:bg-blue-800 p-2 rounded-lg transition-colors"
            >
              ☰
            </button>

            {/* Desktop Buttons - Hidden on Mobile */}
            <div className="hidden md:flex space-x-4">
              <button className="bg-blue-700 hover:bg-blue-800 px-4 py-2 rounded-lg transition-colors">
                Login
              </button>
              <button className="bg-white text-blue-600 hover:bg-blue-50 px-4 py-2 rounded-lg transition-colors">
                Register
              </button>
            </div>
          </div>
        </div>

        {/* Mobile Navigation Menu - Toggleable */}
        {isMobileMenuOpen && (
          <nav className="md:hidden mt-4 pb-4 border-t border-blue-500">
            <div className="flex flex-col space-y-3 pt-4">
              <a href="/caregiver-dashboard" className="hover:text-blue-200 transition-colors py-2">Caregiver Dashboard</a>
              <a href="/elder-dashboard" className="hover:text-blue-200 transition-colors py-2">Elder Dashboard</a>
              <a href="/manage-caregivers" className="hover:text-blue-200 transition-colors py-2">Manage Caregivers</a>
              <a href="/manage-elderly" className="hover:text-blue-200 transition-colors py-2">Manage Elderly</a>
            </div>
          </nav>
        )}
      </div>
    </header>
  );
}

export default Header;