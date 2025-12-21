import { authService } from './authService';
import { API_ENDPOINTS } from '../utils/constants';

class ElderlyService {
  /**
   * Get all elderly for the current user
   * @returns {Promise<Array>} List of elderly
   */
  async getElderly() {
    return await authService.makeAuthenticatedRequest(API_ENDPOINTS.ELDERLY);
  }

  /**
   * Get a specific elderly by ID
   * @param {number} id - Elderly ID
   * @returns {Promise<Object>} Elderly data
   */
  async getElderlyById(id) {
    return await authService.makeAuthenticatedRequest(API_ENDPOINTS.ELDERLY_BY_ID(id));
  }

  /**
   * Add a new elderly person
   * @param {Object} elderlyData - Elderly data to create
   * @returns {Promise<Object>} Created elderly data
   */
  async addElderly(elderlyData) {
    return await authService.makeAuthenticatedRequest(API_ENDPOINTS.ELDERLY, {
      method: 'POST',
      body: JSON.stringify(elderlyData),
    });
  }

  /**
   * Delete an elderly person
   * @param {number} id - Elderly ID
   * @returns {Promise<Object>} Deletion result
   */
  async deleteElderly(id) {
    return await authService.makeAuthenticatedRequest(API_ENDPOINTS.ELDERLY_DELETE(id), {
      method: 'DELETE',
    });
  }
}

export const elderlyService = new ElderlyService();
