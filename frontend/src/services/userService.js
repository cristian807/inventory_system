import { apiClient } from './apiClient';

export const userService = {
  getAll: (skip = 0, limit = 100) => apiClient.get(`/users?skip=${skip}&limit=${limit}`),
  getById: (id) => apiClient.get(`/users/${id}`),
  getWarehouses: (id) => apiClient.get(`/users/${id}/warehouses`),
  getMyWarehouses: () => apiClient.get('/users/me/warehouses'),
  create: (userData) => apiClient.post('/users', userData),
  update: (id, userData) => apiClient.put(`/users/${id}`, userData),
  delete: (id) => apiClient.delete(`/users/${id}`),
  assignWarehouses: (userId, warehouseIds) => apiClient.post(`/users/${userId}/assign-warehouses`, warehouseIds),
  loadBulkUsers: () => apiClient.post('/users/load'),
};
