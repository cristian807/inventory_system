import React, { useState, useEffect } from 'react';
import { warehouseService } from '../services';
import { toast } from 'react-toastify';

function Warehouses({ userRole }) {
  const [warehouses, setWarehouses] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [showModal, setShowModal] = useState(false);
  const [editingWarehouse, setEditingWarehouse] = useState(null);
  
  const [formData, setFormData] = useState({
    name: '',
    location: '',
    capacity: ''
  });

  useEffect(() => {
    fetchWarehouses();
  }, []);

  const fetchWarehouses = async () => {
    setLoading(true);
    try {
      const response = await warehouseService.getAll(0, 100);
      setWarehouses(response.data);
      setError(null);
    } catch (err) {
      toast.error('Error al cargar bodegas: ' + err.message);
    } finally {
      setLoading(false);
    }
  };

  const handleOpenModal = (warehouse = null) => {
    if (warehouse) {
      setEditingWarehouse(warehouse);
      setFormData({
        name: warehouse.name,
        location: warehouse.location || '',
        capacity: warehouse.capacity || ''
      });
    } else {
      setEditingWarehouse(null);
      setFormData({
        name: '',
        location: '',
        capacity: ''
      });
    }
    setShowModal(true);
  };

  const handleCloseModal = () => {
    setShowModal(false);
    setEditingWarehouse(null);
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    
    const dataToSend = {
      ...formData,
      capacity: parseInt(formData.capacity)
    };
    
    try {
      if (editingWarehouse) {
        await warehouseService.update(editingWarehouse.id, dataToSend);
        toast.success('Bodega actualizada correctamente');
      } else {
        await warehouseService.create(dataToSend);
        toast.success('Bodega creada correctamente');
      }
      await fetchWarehouses();
      handleCloseModal();
    } catch (err) {
      toast.error(`Error al ${editingWarehouse ? 'actualizar' : 'crear'} bodega: ` + (err.response?.data?.detail || err.message));
    } finally {
      setLoading(false);
    }
  };

  const handleDelete = async (warehouseId) => {
    if (!confirm('¿Está seguro de que desea eliminar esta bodega?')) {
      return;
    }
    
    setLoading(true);
    try {
      await warehouseService.delete(warehouseId);
      await fetchWarehouses();
      toast.success('Bodega eliminada correctamente');
    } catch (err) {
      toast.error('Error al eliminar bodega: ' + (err.response?.data?.detail || err.message));
    } finally {
      setLoading(false);
    }
  };

  // Solo admin puede crear/editar/eliminar bodegas
  const canModify = userRole === 'admin';

  return (
    <div className="bg-white rounded-lg shadow-md p-6">
      <div className="flex justify-between items-center mb-6">
        <h2 className="text-2xl font-bold text-gray-800">Gestión de Bodegas</h2>
        {canModify && (
          <button
            onClick={() => handleOpenModal()}
            className="bg-gradient-to-r from-indigo-500 to-purple-600 text-white px-6 py-2 rounded-lg hover:shadow-lg transition-all hover:scale-105"
          >
            + Agregar Bodega
          </button>
        )}
      </div>

      {error && (
        <div className="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded mb-4">
          {error}
        </div>
      )}

      {loading && !showModal ? (
        <p className="text-gray-600">Cargando bodegas...</p>
      ) : (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
          {warehouses.map((warehouse) => (
            <div
              key={warehouse.id}
              className="border border-gray-200 rounded-lg p-4 hover:shadow-lg transition-shadow"
            >
              <div className="flex justify-between items-start mb-2">
                <h3 className="text-lg font-bold text-gray-800">{warehouse.name}</h3>
                <span className="text-xs bg-purple-100 text-purple-800 px-2 py-1 rounded-full">
                  ID: {warehouse.id}
                </span>
              </div>
              
              <div className="space-y-2 mb-4">
                <div className="flex items-start gap-2">
                  <span className="text-gray-500 text-sm">📍</span>
                  <p className="text-sm text-gray-600">{warehouse.location || 'Sin ubicación'}</p>
                </div>
                
                <div className="flex items-start gap-2">
                  <span className="text-gray-500 text-sm">📦</span>
                  <p className="text-sm text-gray-600">Capacidad: {warehouse.capacity} m²</p>
                </div>
              </div>

              {canModify && (
                <div className="flex gap-2 pt-3 border-t border-gray-200">
                  <button
                    onClick={() => handleOpenModal(warehouse)}
                    className="flex-1 text-sm text-indigo-600 hover:text-indigo-900 hover:bg-indigo-50 py-2 rounded transition-colors"
                  >
                    ✏️ Editar
                  </button>
                  <button
                    onClick={() => handleDelete(warehouse.id)}
                    className="flex-1 text-sm text-red-600 hover:text-red-900 hover:bg-red-50 py-2 rounded transition-colors"
                  >
                    🗑️ Eliminar
                  </button>
                </div>
              )}
            </div>
          ))}
        </div>
      )}

      {warehouses.length === 0 && !loading && (
        <div className="text-center py-12">
          <div className="text-6xl mb-4">🏢</div>
          <p className="text-gray-600 mb-4">No hay bodegas registradas</p>
          {canModify && (
            <button
              onClick={() => handleOpenModal()}
              className="bg-gradient-to-r from-indigo-500 to-purple-600 text-white px-6 py-2 rounded-lg hover:shadow-lg transition-all"
            >
              Crear primera bodega
            </button>
          )}
        </div>
      )}

      {/* Modal para crear/editar bodega */}
      {showModal && (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
          <div className="bg-white rounded-lg shadow-xl p-6 w-full max-w-md">
            <h3 className="text-xl font-bold text-gray-800 mb-4">
              {editingWarehouse ? 'Editar Bodega' : 'Nueva Bodega'}
            </h3>
            
            <form onSubmit={handleSubmit}>
              <div className="space-y-4">
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">
                    Nombre *
                  </label>
                  <input
                    type="text"
                    value={formData.name}
                    onChange={(e) => setFormData({ ...formData, name: e.target.value })}
                    className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-purple-500 focus:border-transparent"
                    placeholder="Ej: Bodega Principal"
                    required
                  />
                </div>

                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">
                    Ubicación *
                  </label>
                  <input
                    type="text"
                    value={formData.location}
                    onChange={(e) => setFormData({ ...formData, location: e.target.value })}
                    className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-purple-500 focus:border-transparent"
                    placeholder="Ej: Carrera 7 # 45-23, Bogotá"
                    required
                  />
                </div>

                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">
                    Capacidad (m²) *
                  </label>
                  <input
                    type="number"
                    value={formData.capacity}
                    onChange={(e) => setFormData({ ...formData, capacity: e.target.value })}
                    className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-purple-500 focus:border-transparent"
                    placeholder="Ej: 500"
                    min="1"
                    required
                  />
                </div>
              </div>

              <div className="flex justify-end gap-3 mt-6">
                <button
                  type="button"
                  onClick={handleCloseModal}
                  className="px-4 py-2 border border-gray-300 rounded-lg text-gray-700 hover:bg-gray-50"
                >
                  Cancelar
                </button>
                <button
                  type="submit"
                  disabled={loading}
                  className="px-4 py-2 bg-gradient-to-r from-indigo-500 to-purple-600 text-white rounded-lg hover:shadow-lg transition-all disabled:opacity-50"
                >
                  {loading ? 'Guardando...' : (editingWarehouse ? 'Actualizar' : 'Crear')}
                </button>
              </div>
            </form>
          </div>
        </div>
      )}
    </div>
  );
}

export default Warehouses;
