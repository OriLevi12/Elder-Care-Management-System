import React, { useState } from 'react';
import { useNavigate, Link } from 'react-router-dom';
import { useAuth } from '../../contexts/AuthContext';

function Header() {
  const [isMobileMenuOpen, setIsMobileMenuOpen] = useState(false);
  const [isUserMenuOpen, setIsUserMenuOpen] = useState(false);
  const navigate = useNavigate();
  const { user, logout, isAuthenticated } = useAuth();
  
  const toggleMobileMenu = () => {
    setIsMobileMenuOpen(!isMobileMenuOpen);
  };

  const toggleUserMenu = () => {
    setIsUserMenuOpen(!isUserMenuOpen);
  };

  const handleLogout = () => {
    logout();
    navigate('/login');
    setIsUserMenuOpen(false);
  };

  const handleLogin = () => {
    navigate('/login');
  };

  const handleRegister = () => {
    navigate('/register');
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
            <Link to="/" className="hover:text-blue-200 transition-colors">Home</Link>
            <Link to="/caregiver-dashboard" className="hover:text-blue-200 transition-colors">Caregiver Dashboard</Link>
            <Link to="/elder-dashboard" className="hover:text-blue-200 transition-colors">Elder Dashboard</Link>
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
              {isAuthenticated ? (
                <div className="relative">
                  <button 
                    onClick={toggleUserMenu}
                    className="flex items-center space-x-2 bg-blue-700 hover:bg-blue-800 px-4 py-2 rounded-lg transition-colors"
                  >
                    <span>👤</span>
                    <span>{user?.full_name || 'User'}</span>
                    <span>▼</span>
                  </button>
                  
                  {isUserMenuOpen && (
                    <div className="absolute right-0 mt-2 w-48 bg-white rounded-md shadow-lg py-1 z-50">
                      <div className="px-4 py-2 text-sm text-gray-700 border-b">
                        <div className="font-medium">{user?.full_name}</div>
                        <div className="text-gray-500">{user?.email}</div>
                      </div>
                      <button
                        onClick={handleLogout}
                        className="block w-full text-left px-4 py-2 text-sm text-gray-700 hover:bg-gray-100"
                      >
                        Sign out
                      </button>
                    </div>
                  )}
                </div>
              ) : (
                <>
                  <button 
                    onClick={handleLogin}
                    className="bg-blue-700 hover:bg-blue-800 px-4 py-2 rounded-lg transition-colors"
                  >
                    Login
                  </button>
                  <button 
                    onClick={handleRegister}
                    className="bg-white text-blue-600 hover:bg-blue-50 px-4 py-2 rounded-lg transition-colors"
                  >
                    Register
                  </button>
                </>
              )}
            </div>
          </div>
        </div>

        {/* Mobile Navigation Menu - Toggleable */}
        {isMobileMenuOpen && (
          <nav className="md:hidden mt-4 pb-4 border-t border-blue-500">
            <div className="flex flex-col space-y-3 pt-4">
              <Link to="/" className="hover:text-blue-200 transition-colors py-2" onClick={() => setIsMobileMenuOpen(false)}>Home</Link>
              <Link to="/caregiver-dashboard" className="hover:text-blue-200 transition-colors py-2" onClick={() => setIsMobileMenuOpen(false)}>Caregiver Dashboard</Link>
              <Link to="/elder-dashboard" className="hover:text-blue-200 transition-colors py-2" onClick={() => setIsMobileMenuOpen(false)}>Elder Dashboard</Link>
              
              {/* Mobile Auth Buttons */}
              <div className="pt-4 border-t border-blue-500">
                {isAuthenticated ? (
                  <div className="space-y-2">
                    <div className="text-sm text-blue-200">
                      <div className="font-medium">{user?.full_name}</div>
                      <div className="text-xs">{user?.email}</div>
                    </div>
                    <button
                      onClick={handleLogout}
                      className="w-full bg-blue-700 hover:bg-blue-800 px-4 py-2 rounded-lg transition-colors text-left"
                    >
                      Sign out
                    </button>
                  </div>
                ) : (
                  <div className="space-y-2">
                    <button 
                      onClick={handleLogin}
                      className="w-full bg-blue-700 hover:bg-blue-800 px-4 py-2 rounded-lg transition-colors text-left"
                    >
                      Login
                    </button>
                    <button 
                      onClick={handleRegister}
                      className="w-full bg-white text-blue-600 hover:bg-blue-50 px-4 py-2 rounded-lg transition-colors text-left"
                    >
                      Register
                    </button>
                  </div>
                )}
              </div>
            </div>
          </nav>
        )}
      </div>
    </header>
  );
}

export default Header;