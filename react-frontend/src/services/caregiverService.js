import { authService } from './authService';
import { API_ENDPOINTS } from '../utils/constants';

class CaregiverService {
  /**
   * Get all caregivers for the current user
   * @returns {Promise<Array>} List of caregivers
   */
  async getCaregivers() {
    return await authService.makeAuthenticatedRequest(API_ENDPOINTS.CAREGIVERS);
  }

  /**
   * Get a specific caregiver by ID
   * @param {number} id - Caregiver ID
   * @returns {Promise<Object>} Caregiver data
   */
  async getCaregiverById(id) {
    return await authService.makeAuthenticatedRequest(`/caregivers/${id}`);
  }

  /**
   * Add a new caregiver
   * @param {Object} caregiverData - Caregiver data to create
   * @returns {Promise<Object>} Created caregiver data
   */
  async addCaregiver(caregiverData) {
    return await authService.makeAuthenticatedRequest('/caregivers/', {
      method: 'POST',
      body: JSON.stringify(caregiverData),
    });
  }

  /**
   * Update caregiver salary
   * @param {number} id - Caregiver ID
   * @param {Object} salaryData - Salary data to update
   * @returns {Promise<Object>} Updated caregiver data
   */
  async updateCaregiverSalary(id, salaryData) {
    return await authService.makeAuthenticatedRequest(`/caregivers/${id}/update-salary`, {
      method: 'PUT',
      body: JSON.stringify(salaryData),
    });
  }

  /**
   * Delete a caregiver
   * @param {number} id - Caregiver ID
   * @returns {Promise<Object>} Deletion result
   */
  async deleteCaregiver(id) {
    return await authService.makeAuthenticatedRequest(`/caregivers/${id}`, {
      method: 'DELETE',
    });
  }

  /**
   * Generate PDF for a caregiver
   * @param {number} id - Caregiver ID
   * @returns {Promise<Blob>} PDF file blob
   */
  async generateCaregiverPDF(id) {
    const token = localStorage.getItem('token');
    const response = await fetch(`${process.env.REACT_APP_API_URL || 'http://localhost:8000'}/caregivers/${id}/generate-pdf`, {
      method: 'GET',
      headers: {
        'Authorization': `Bearer ${token}`,
        'Accept': 'application/pdf',
      },
    });

    if (!response.ok) {
      if (response.status === 401) {
        localStorage.removeItem('token');
        window.location.href = '/login';
        throw new Error('Authentication required');
      }
      throw new Error(`HTTP error! status: ${response.status}`);
    }

    return await response.blob();
  }
}

export const caregiverService = new CaregiverService();
