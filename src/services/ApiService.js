/**
 * API Service for communicating with Python backend
 */

const API_BASE_URL = __DEV__ 
  ? 'http://localhost:5000/api'  // Development
  : 'https://your-production-server.com/api';  // Production

class ApiService {
  
  /**
   * Make a generic API request
   */
  async request(endpoint, options = {}) {
    const url = `${API_BASE_URL}${endpoint}`;
    
    const defaultOptions = {
      headers: {
        'Content-Type': 'application/json',
        'Accept': 'application/json',
      },
    };
    
    const finalOptions = { ...defaultOptions, ...options };
    
    try {
      const response = await fetch(url, finalOptions);
      
      if (!response.ok) {
        const errorData = await response.json().catch(() => ({}));
        throw new Error(errorData.error || `HTTP ${response.status}: ${response.statusText}`);
      }
      
      return await response.json();
    } catch (error) {
      console.error(`API Error for ${endpoint}:`, error);
      throw error;
    }
  }
  
  /**
   * Check if Python backend is healthy
   */
  async checkHealth() {
    return this.request('/health');
  }
  
  /**
   * Get users from backend
   */
  async getUsers() {
    return this.request('/users');
  }
  
  /**
   * Create a new user
   */
  async createUser(userData) {
    return this.request('/users', {
      method: 'POST',
      body: JSON.stringify(userData),
    });
  }
  
  /**
   * Process data using Python backend
   */
  async processData(data) {
    return this.request('/process', {
      method: 'POST',
      body: JSON.stringify(data),
    });
  }
  
  /**
   * Get predictions from ML service
   */
  async getPrediction(features) {
    return this.request('/predict', {
      method: 'POST',
      body: JSON.stringify({ features }),
    });
  }
  
  /**
   * Process numerical data
   */
  async processNumbers(numbers) {
    return this.processData({ numbers });
  }
  
  /**
   * Process text data
   */
  async processText(text) {
    return this.processData({ text });
  }
  
  /**
   * Process dataset
   */
  async processDataset(dataset) {
    return this.processData({ dataset });
  }
}

// Export singleton instance
const apiService = new ApiService();
export default apiService;
