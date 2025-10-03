// Application constants
export const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000';

// Route paths
export const ROUTES = {
  HOME: '/',
  LOGIN: '/login',
  REGISTER: '/register',
  CAREGIVER_DASHBOARD: '/caregiver-dashboard',
  ELDER_DASHBOARD: '/elder-dashboard',
  MANAGE_CAREGIVERS: '/manage-caregivers',
  MANAGE_ELDERLY: '/manage-elderly',
};

// Local storage keys
export const STORAGE_KEYS = {
  TOKEN: 'token',
  USER: 'user',
};

// API endpoints
export const API_ENDPOINTS = {
  AUTH: {
    LOGIN: '/auth/login',
    REGISTER: '/auth/register',
    ME: '/auth/me',
  },
  CAREGIVERS: '/caregivers',
  ELDERLY: '/elderly',
  CAREGIVER_ASSIGNMENTS: '/caregiver-assignments',
};
