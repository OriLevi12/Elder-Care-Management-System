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
  CAREGIVER_BY_ID: (id) => `/caregivers/${id}`,
  CAREGIVER_UPDATE_SALARY: (id) => `/caregivers/${id}/update-salary`,
  CAREGIVER_GENERATE_PDF: (id) => `/caregivers/${id}/generate-pdf`,
  CAREGIVER_DELETE: (id) => `/caregivers/${id}`,
  ELDERLY: '/elderly',
  ELDERLY_BY_ID: (id) => `/elderly/${id}`,
  ELDERLY_DELETE: (id) => `/elderly/${id}`,
  ELDERLY_ADD_TASK: (id) => `/elderly/${id}/tasks`,
  ELDERLY_ADD_MEDICATION: (id) => `/elderly/${id}/medications`,
  CAREGIVER_ASSIGNMENTS: '/caregiver-assignments',
  CAREGIVER_ASSIGNMENT_DELETE: (id) => `/caregiver-assignments/${id}`,
};
