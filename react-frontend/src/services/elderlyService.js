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

  /**
   * Add a task to an elderly person
   * @param {number} elderlyId - Elderly ID
   * @param {Object} taskData - Task data (description, status)
   * @returns {Promise<Object>} Created task data
   */
  async addTask(elderlyId, taskData) {
    return await authService.makeAuthenticatedRequest(API_ENDPOINTS.ELDERLY_ADD_TASK(elderlyId), {
      method: 'POST',
      body: JSON.stringify(taskData),
    });
  }

  /**
   * Add a medication to an elderly person
   * @param {number} elderlyId - Elderly ID
   * @param {Object} medicationData - Medication data (name, dosage, frequency)
   * @returns {Promise<Object>} Created medication data
   */
  async addMedication(elderlyId, medicationData) {
    return await authService.makeAuthenticatedRequest(API_ENDPOINTS.ELDERLY_ADD_MEDICATION(elderlyId), {
      method: 'POST',
      body: JSON.stringify(medicationData),
    });
  }
}

export const elderlyService = new ElderlyService();
