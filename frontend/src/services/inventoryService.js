import { apiClient } from './apiClient';

export const inventoryService = {
  getAll: (warehouse_id = null, status = null) => {
    let url = '/inventory-counts/';
    const params = new URLSearchParams();
    if (warehouse_id) params.append('warehouse_id', warehouse_id);
    if (status) params.append('status', status);
    if (params.toString()) url += '?' + params.toString();
    
    return apiClient.get(url);
  },
  getDetail: (id) => apiClient.get(`/inventory-counts/${id}`),
  create: (countData) => apiClient.post('/inventory-counts/', countData),
  close: (id) => apiClient.put(`/inventory-counts/${id}/close`, {}),
  addItem: (countId, itemData) => apiClient.post(`/inventory-counts/${countId}/items`, itemData),
  getItems: (countId) => apiClient.get(`/inventory-counts/${countId}/items`),
};
