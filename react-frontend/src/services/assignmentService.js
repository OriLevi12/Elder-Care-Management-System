import { API_BASE_URL, API_ENDPOINTS, STORAGE_KEYS } from '../utils/constants';

/**
 * Service for handling caregiver-elderly assignment operations
 */
class AssignmentService {
  /**
   * Get all caregiver assignments for the current user
   * @returns {Promise<Array>} Array of assignment objects
   */
  async getAssignments() {
    const token = localStorage.getItem(STORAGE_KEYS.TOKEN);
    
    if (!token) {
      throw new Error('Authentication required');
    }

    try {
      const response = await fetch(`${API_BASE_URL}${API_ENDPOINTS.CAREGIVER_ASSIGNMENTS}`, {
        method: 'GET',
        headers: {
          'Authorization': `Bearer ${token}`,
          'Content-Type': 'application/json',
        },
      });

      if (!response.ok) {
        if (response.status === 401) {
          localStorage.removeItem(STORAGE_KEYS.TOKEN);
          window.location.href = '/login';
          throw new Error('Authentication required');
        }
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      return await response.json();
    } catch (error) {
      if (error.name === 'TypeError' && error.message.includes('fetch')) {
        throw new Error('Unable to connect to server. Please check if the backend is running.');
      }
      throw error;
    }
  }

  /**
   * Get elderly assigned to a specific caregiver
   * @param {number} caregiverId - The ID of the caregiver
   * @returns {Promise<Array>} Array of elderly objects assigned to the caregiver
   */
  async getElderlyForCaregiver(caregiverId) {
    try {
      // Get all assignments
      const assignments = await this.getAssignments();
      
      // Filter assignments for the specific caregiver
      const caregiverAssignments = assignments.filter(
        assignment => assignment.caregiver_id === caregiverId
      );
      
      // Extract elderly IDs
      const elderlyIds = caregiverAssignments.map(assignment => assignment.elderly_id);
      
      // Get elderly details for each ID
      const elderlyPromises = elderlyIds.map(elderlyId => this.getElderlyById(elderlyId));
      const elderlyList = await Promise.all(elderlyPromises);
      
      return elderlyList;
    } catch (error) {
      console.error('Error getting elderly for caregiver:', error);
      throw error;
    }
  }

  /**
   * Get elderly person by ID
   * @param {number} elderlyId - The ID of the elderly person
   * @returns {Promise<Object>} Elderly object
   */
  async getElderlyById(elderlyId) {
    const token = localStorage.getItem(STORAGE_KEYS.TOKEN);
    
    if (!token) {
      throw new Error('Authentication required');
    }

    try {
      const response = await fetch(`${API_BASE_URL}${API_ENDPOINTS.ELDERLY_BY_ID(elderlyId)}`, {
        method: 'GET',
        headers: {
          'Authorization': `Bearer ${token}`,
          'Content-Type': 'application/json',
        },
      });

      if (!response.ok) {
        if (response.status === 401) {
          localStorage.removeItem(STORAGE_KEYS.TOKEN);
          window.location.href = '/login';
          throw new Error('Authentication required');
        }
        if (response.status === 404) {
          throw new Error('Elderly person not found');
        }
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      return await response.json();
    } catch (error) {
      if (error.name === 'TypeError' && error.message.includes('fetch')) {
        throw new Error('Unable to connect to server. Please check if the backend is running.');
      }
      throw error;
    }
  }

  /**
   * Get caregiver by ID
   * @param {number} caregiverId - The ID of the caregiver
   * @returns {Promise<Object>} Caregiver object
   */
  async getCaregiverById(caregiverId) {
    const token = localStorage.getItem(STORAGE_KEYS.TOKEN);
    
    if (!token) {
      throw new Error('Authentication required');
    }

    try {
      const response = await fetch(`${API_BASE_URL}${API_ENDPOINTS.CAREGIVER_BY_ID(caregiverId)}`, {
        method: 'GET',
        headers: {
          'Authorization': `Bearer ${token}`,
          'Content-Type': 'application/json',
        },
      });

      if (!response.ok) {
        if (response.status === 401) {
          localStorage.removeItem(STORAGE_KEYS.TOKEN);
          window.location.href = '/login';
          throw new Error('Authentication required');
        }
        if (response.status === 404) {
          throw new Error('Caregiver not found');
        }
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      return await response.json();
    } catch (error) {
      if (error.name === 'TypeError' && error.message.includes('fetch')) {
        throw new Error('Unable to connect to server. Please check if the backend is running.');
      }
      throw error;
    }
  }

  /**
   * Get caregivers assigned to a specific elderly person
   * @param {number} elderlyId - The ID of the elderly person
   * @returns {Promise<Array>} Array of caregiver objects assigned to the elderly person
   */
  async getCaregiversForElderly(elderlyId) {
    try {
      // Get all assignments
      const assignments = await this.getAssignments();
      
      // Filter assignments for the specific elderly person
      const elderlyAssignments = assignments.filter(
        assignment => assignment.elderly_id === elderlyId
      );
      
      // Extract caregiver IDs
      const caregiverIds = elderlyAssignments.map(assignment => assignment.caregiver_id);
      
      // Get caregiver details for each ID
      const caregiverPromises = caregiverIds.map(caregiverId => this.getCaregiverById(caregiverId));
      const caregiverList = await Promise.all(caregiverPromises);
      
      return caregiverList;
    } catch (error) {
      console.error('Error getting caregivers for elderly:', error);
      throw error;
    }
  }

  /**
   * Create a new caregiver-elderly assignment
   * @param {number} caregiverId - The ID of the caregiver
   * @param {number} elderlyId - The ID of the elderly person
   * @returns {Promise<Object>} The created assignment
   */
  async createAssignment(caregiverId, elderlyId) {
    const token = localStorage.getItem(STORAGE_KEYS.TOKEN);
    
    if (!token) {
      throw new Error('Authentication required');
    }

    try {
      const response = await fetch(`${API_BASE_URL}${API_ENDPOINTS.CAREGIVER_ASSIGNMENTS}`, {
        method: 'POST',
        headers: {
          'Authorization': `Bearer ${token}`,
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          caregiver_id: caregiverId,
          elderly_id: elderlyId
        }),
      });

      if (!response.ok) {
        if (response.status === 401) {
          localStorage.removeItem(STORAGE_KEYS.TOKEN);
          window.location.href = '/login';
          throw new Error('Authentication required');
        }
        if (response.status === 400) {
          const errorData = await response.json();
          throw new Error(errorData.detail || 'Invalid assignment data');
        }
        if (response.status === 404) {
          throw new Error('Caregiver or elderly person not found');
        }
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      return await response.json();
    } catch (error) {
      if (error.name === 'TypeError' && error.message.includes('fetch')) {
        throw new Error('Unable to connect to server. Please check if the backend is running.');
      }
      throw error;
    }
  }

  /**
   * Delete a caregiver-elderly assignment
   * @param {number} caregiverId - The ID of the caregiver
   * @param {number} elderlyId - The ID of the elderly person
   * @returns {Promise<Object>} Success message
   */
  async deleteAssignment(caregiverId, elderlyId) {
    const token = localStorage.getItem(STORAGE_KEYS.TOKEN);
    
    if (!token) {
      throw new Error('Authentication required');
    }

    try {
      // First, get all assignments to find the assignment ID
      const assignments = await this.getAssignments();
      const assignment = assignments.find(
        a => a.caregiver_id === caregiverId && a.elderly_id === elderlyId
      );

      if (!assignment) {
        throw new Error('Assignment not found');
      }

      const response = await fetch(`${API_BASE_URL}${API_ENDPOINTS.CAREGIVER_ASSIGNMENT_DELETE(assignment.id)}`, {
        method: 'DELETE',
        headers: {
          'Authorization': `Bearer ${token}`,
          'Content-Type': 'application/json',
        },
      });

      if (!response.ok) {
        if (response.status === 401) {
          localStorage.removeItem(STORAGE_KEYS.TOKEN);
          window.location.href = '/login';
          throw new Error('Authentication required');
        }
        if (response.status === 404) {
          throw new Error('Assignment not found');
        }
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      return await response.json();
    } catch (error) {
      if (error.name === 'TypeError' && error.message.includes('fetch')) {
        throw new Error('Unable to connect to server. Please check if the backend is running.');
      }
      throw error;
    }
  }

  /**
   * Get all elderly people for assignment (including already assigned ones)
   * @param {number} caregiverId - The ID of the caregiver to check assignments for
   * @returns {Promise<Array>} Array of elderly objects with assignment status
   */
  async getAllElderlyForAssignment(caregiverId) {
    try {
      // Get all elderly and assignments for this caregiver
      const [allElderly, caregiverAssignments] = await Promise.all([
        this.getAllElderly(),
        this.getElderlyForCaregiver(caregiverId)
      ]);

      // Get IDs of elderly already assigned to this caregiver
      const assignedElderlyIds = caregiverAssignments.map(elderly => elderly.id);

      // Add assignment status to each elderly
      const elderlyWithStatus = allElderly.map(elderly => ({
        ...elderly,
        isAssignedToThisCaregiver: assignedElderlyIds.includes(elderly.id)
      }));

      return elderlyWithStatus;
    } catch (error) {
      console.error('Error getting elderly for assignment:', error);
      throw error;
    }
  }

  /**
   * Get all elderly people for the current user
   * @returns {Promise<Array>} Array of elderly objects
   */
  async getAllElderly() {
    const token = localStorage.getItem(STORAGE_KEYS.TOKEN);
    
    if (!token) {
      throw new Error('Authentication required');
    }

    try {
      const response = await fetch(`${API_BASE_URL}${API_ENDPOINTS.ELDERLY}`, {
        method: 'GET',
        headers: {
          'Authorization': `Bearer ${token}`,
          'Content-Type': 'application/json',
        },
      });

      if (!response.ok) {
        if (response.status === 401) {
          localStorage.removeItem(STORAGE_KEYS.TOKEN);
          window.location.href = '/login';
          throw new Error('Authentication required');
        }
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      return await response.json();
    } catch (error) {
      if (error.name === 'TypeError' && error.message.includes('fetch')) {
        throw new Error('Unable to connect to server. Please check if the backend is running.');
      }
      throw error;
    }
  }
}

export default new AssignmentService();