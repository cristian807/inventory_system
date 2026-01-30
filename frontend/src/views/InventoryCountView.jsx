import React, { useState, useEffect } from 'react';
import { inventoryService, productService, warehouseService, userService } from '../services';
import { toast } from 'react-toastify';

function InventoryCount({ token, userRole }) {
  const [counts, setCounts] = useState([]);
  const [products, setProducts] = useState([]);
  const [warehouses, setWarehouses] = useState([]);
  const [userWarehouses, setUserWarehouses] = useState([]); // Bodegas asignadas al usuario
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [success, setSuccess] = useState(null);
  
  const isAdmin = userRole === 'admin';
  
  // Form states
  const [showCreateForm, setShowCreateForm] = useState(false);
  const [selectedCount, setSelectedCount] = useState(null);
  const [countForm, setCountForm] = useState({
    name: '',
    cut_off_date: '',
    warehouse_id: ''
  });
  
  // Item form states
  const [itemForm, setItemForm] = useState({
    product_id: '',
    packages_count: 1
  });
  
  const [calculatedUnits, setCalculatedUnits] = useState(0);
  const [countDetails, setCountDetails] = useState(null);

  // Cargar bodegas primero
  useEffect(() => {
    fetchWarehouses();
    fetchProducts();
  }, []);

  // Cargar conteos después de tener las bodegas
  useEffect(() => {
    if (userWarehouses.length > 0 || isAdmin) {
      fetchCounts();
    }
  }, [userWarehouses, isAdmin]);

  useEffect(() => {
    calculateUnits();
  }, [itemForm.product_id, itemForm.packages_count, products]);

  const fetchCounts = async () => {
    setLoading(true);
    try {
      const response = await inventoryService.getAll();
      let countsData = response.data;
      
      // Si no es admin, filtrar solo conteos de bodegas asignadas
      if (!isAdmin && userWarehouses.length > 0) {
        const warehouseIds = userWarehouses.map(w => w.id);
        countsData = countsData.filter(count => warehouseIds.includes(count.warehouse_id));
      }
      
      setCounts(countsData);
    } catch (err) {
      toast.error('Error al cargar conteos: ' + err.message);
    } finally {
      setLoading(false);
    }
  };

  const fetchProducts = async () => {
    try {
      const response = await productService.getAll(0, 1000);
      setProducts(response.data);
    } catch (err) {
      console.error('Error al cargar productos:', err);
    }
  };

  const fetchWarehouses = async () => {
    try {
      // ADMIN: obtiene todas las bodegas
      // USER: obtiene solo sus bodegas asignadas
      if (isAdmin) {
        const response = await warehouseService.getAll(0, 1000);
        setWarehouses(response.data);
        setUserWarehouses(response.data);
      } else {
        const response = await userService.getMyWarehouses();
        const assignedWarehouses = response.data.assigned_warehouses || [];
        setWarehouses(assignedWarehouses);
        setUserWarehouses(assignedWarehouses);
      }
    } catch (err) {
      console.error('Error al cargar bodegas:', err);
      toast.error('Error al cargar bodegas: ' + err.message);
    }
  };

  const fetchCountDetails = async (countId) => {
    try {
      const response = await inventoryService.getDetail(countId);
      const countData = response.data;
      
      // Validar que el usuario tenga acceso a la bodega del conteo
      if (!isAdmin) {
        const warehouseIds = userWarehouses.map(w => w.id);
        if (!warehouseIds.includes(countData.warehouse_id)) {
          toast.error('⛔ No tienes permisos para ver este conteo');
          return;
        }
      }
      
      setCountDetails(countData);
      setSelectedCount(countId);
    } catch (err) {
      toast.error('Error al cargar detalles del conteo: ' + err.message);
    }
  };

  const calculateUnits = () => {
    if (itemForm.product_id && itemForm.packages_count) {
      const product = products.find(p => p.id === parseInt(itemForm.product_id));
      if (product) {
        const units = itemForm.packages_count * (product.units_per_package || 1);
        setCalculatedUnits(units);
      }
    } else {
      setCalculatedUnits(0);
    }
  };

  const handleCreateCount = async (e) => {
    e.preventDefault();
    
    // Validar que el usuario tenga acceso a la bodega seleccionada
    if (!isAdmin) {
      const warehouseId = parseInt(countForm.warehouse_id);
      const hasAccess = userWarehouses.some(w => w.id === warehouseId);
      if (!hasAccess) {
        toast.error('⛔ No tienes permisos para crear conteos en esta bodega');
        return;
      }
    }
    
    setLoading(true);
    try {
      await inventoryService.create(countForm);
      toast.success('✅ Conteo creado exitosamente');
      setShowCreateForm(false);
      setCountForm({ name: '', cut_off_date: '', warehouse_id: '' });
      fetchCounts();
    } catch (err) {
      toast.error('Error al crear conteo: ' + err.message);
    } finally {
      setLoading(false);
    }
  };

  const handleAddItem = async (e) => {
    e.preventDefault();
    if (!selectedCount) {
      toast.error('Selecciona un conteo primero');
      return;
    }
    
    // Validar que el usuario tenga acceso a la bodega del conteo
    const selectedCountData = counts.find(c => c.id === selectedCount);
    if (!isAdmin && selectedCountData) {
      const warehouseIds = userWarehouses.map(w => w.id);
      if (!warehouseIds.includes(selectedCountData.warehouse_id)) {
        toast.error('⛔ No tienes permisos para agregar items a este conteo');
        return;
      }
    }
    
    setLoading(true);
    try {
      const warehouse = warehouses.find(w => w.id === selectedCountData?.warehouse_id);
      const itemData = {
        ...itemForm,
        warehouse_id: warehouse?.id
      };
      
      await inventoryService.addItem(selectedCount, itemData);
      toast.success('✅ Item agregado al conteo');
      setItemForm({ product_id: '', packages_count: 1 });
      fetchCountDetails(selectedCount);
    } catch (err) {
      toast.error('Error al agregar item: ' + err.message);
    } finally {
      setLoading(false);
    }
  };

  const handleCloseCount = async (countId) => {
    if (!window.confirm('¿Estás seguro de cerrar este conteo? Esta acción no se puede deshacer.')) {
      return;
    }
    
    setLoading(true);
    try {
      await inventoryService.close(countId);
      toast.success('Conteo cerrado exitosamente');
      fetchCounts();
      if (selectedCount === countId) {
        fetchCountDetails(countId);
      }
    } catch (err) {
      toast.error('Error al cerrar conteo: ' + err.message);
    } finally {
      setLoading(false);
    }
  };

  const getSelectedProduct = () => {
    return products.find(p => p.id === parseInt(itemForm.product_id));
  };

  return (
    <div className="space-y-6">
      <div className="flex justify-between items-center bg-white rounded-lg shadow-md p-6">
        <h2 className="text-2xl font-bold text-gray-800">Conteos de Inventario</h2>
        <button 
          className="px-6 py-2 bg-gradient-to-r from-indigo-500 to-purple-600 text-white rounded-lg font-semibold hover:shadow-lg transform hover:scale-105 transition-all disabled:opacity-50"
          onClick={() => setShowCreateForm(!showCreateForm)}
          disabled={loading || (!isAdmin && userWarehouses.length === 0)}
          title={!isAdmin && userWarehouses.length === 0 ? 'No tienes bodegas asignadas' : ''}
        >
          {showCreateForm ? 'Cancelar' : '+ Nuevo Conteo'}
        </button>
      </div>

      {/* Mensaje informativo para usuarios sin bodegas asignadas */}
      {!isAdmin && userWarehouses.length === 0 && (
        <div className="bg-yellow-50 border-l-4 border-yellow-500 p-6 rounded-lg">
          <div className="flex items-start">
            <span className="text-2xl mr-3">⚠️</span>
            <div>
              <h3 className="text-yellow-800 font-bold text-lg mb-2">Sin bodegas asignadas</h3>
              <p className="text-yellow-700">No tienes bodegas asignadas. Contacta a un administrador para que te asigne las bodegas en las que puedes realizar conteos de inventario.</p>
            </div>
          </div>
        </div>
      )}

      {/* Mensaje informativo para usuarios normales */}
      {!isAdmin && userWarehouses.length > 0 && (
        <div className="bg-blue-50 border-l-4 border-blue-500 p-4 rounded-lg">
          <p className="text-blue-700">
            <strong>ℹ️ Información:</strong> Solo puedes crear conteos en las {userWarehouses.length} bodega(s) asignada(s) a tu usuario: {userWarehouses.map(w => w.name).join(', ')}.
          </p>
        </div>
      )}

      {error && (
        <div className="bg-red-100 border-l-4 border-red-500 text-red-700 p-4 rounded">
          {error}
        </div>
      )}
      {success && (
        <div className="bg-green-100 border-l-4 border-green-500 text-green-700 p-4 rounded">
          {success}
        </div>
      )}

      {showCreateForm && (
        <div className="bg-white rounded-lg shadow-md p-6">
          <h3 className="text-xl font-bold text-gray-800 mb-4">Crear Nuevo Conteo</h3>
          <form onSubmit={handleCreateCount} className="space-y-4">
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">Nombre del Conteo *</label>
              <input
                type="text"
                value={countForm.name}
                onChange={(e) => setCountForm({ ...countForm, name: e.target.value })}
                placeholder="Ej: Conteo Enero 2026"
                required
                className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-purple-500 focus:border-transparent"
              />
            </div>
            
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">Fecha de Corte *</label>
              <input
                type="date"
                value={countForm.cut_off_date}
                onChange={(e) => setCountForm({ ...countForm, cut_off_date: e.target.value })}
                required
                className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-purple-500 focus:border-transparent"
              />
            </div>
            
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">Bodega *</label>
              <select
                value={countForm.warehouse_id}
                onChange={(e) => setCountForm({ ...countForm, warehouse_id: e.target.value })}
                required
                className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-purple-500 focus:border-transparent"
              >
                <option value="">Selecciona una bodega</option>
                {warehouses.map(w => (
                  <option key={w.id} value={w.id}>
                    {w.name} - {w.location}
                  </option>
                ))}
              </select>
            </div>
            
            <div className="flex gap-2">
              <button 
                type="submit" 
                className="px-6 py-2 bg-gradient-to-r from-indigo-500 to-purple-600 text-white rounded-lg font-semibold hover:shadow-lg transition-all disabled:opacity-50"
                disabled={loading}
              >
                {loading ? 'Creando...' : 'Crear Conteo'}
              </button>
              <button 
                type="button" 
                className="px-6 py-2 bg-gray-500 text-white rounded-lg font-semibold hover:bg-gray-600 transition-all"
                onClick={() => setShowCreateForm(false)}
              >
                Cancelar
              </button>
            </div>
          </form>
        </div>
      )}

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <div className="bg-white rounded-lg shadow-md p-6">
          <h3 className="text-xl font-bold text-gray-800 mb-4">Lista de Conteos</h3>
          {loading && counts.length === 0 ? (
            <p className="text-gray-600">Cargando conteos...</p>
          ) : counts.length === 0 ? (
            <p className="text-gray-500 italic">No hay conteos registrados</p>
          ) : (
            <div className="space-y-3">
              {counts.map(count => (
                <div 
                  key={count.id} 
                  className={`border rounded-lg p-4 cursor-pointer transition-all ${
                    selectedCount === count.id 
                      ? 'border-purple-500 bg-purple-50 shadow-md' 
                      : 'border-gray-200 hover:border-purple-300 hover:shadow'
                  } ${count.status === 'closed' ? 'opacity-75' : ''}`}
                  onClick={() => fetchCountDetails(count.id)}
                >
                  <div className="flex justify-between items-start mb-2">
                    <h4 className="font-bold text-gray-800">{count.name}</h4>
                    <span className={`text-xs px-3 py-1 rounded-full font-semibold ${
                      count.status === 'in_progress' ? 'bg-blue-100 text-blue-700' : 
                      count.status === 'completed' ? 'bg-green-100 text-green-700' : 
                      'bg-gray-100 text-gray-700'
                    }`}>
                      {count.status === 'in_progress' ? 'En Progreso' : 
                       count.status === 'completed' ? 'Completado' : 'Cerrado'}
                    </span>
                  </div>
                  <div className="space-y-1 text-sm text-gray-600">
                    <p><strong className="text-gray-700">Bodega:</strong> {count.warehouse_name}</p>
                    <p><strong className="text-gray-700">Fecha de corte:</strong> {count.cut_off_date}</p>
                    <p><strong className="text-gray-700">Items:</strong> {count.items_count}</p>
                    <p><strong className="text-gray-700">Creado por:</strong> {count.creator_name}</p>
                  </div>
                  {isAdmin && count.status !== 'closed' && (
                    <button
                      className="mt-3 w-full px-4 py-2 bg-red-500 text-white text-sm rounded-lg hover:bg-red-600 transition-all"
                      onClick={(e) => {
                        e.stopPropagation();
                        handleCloseCount(count.id);
                      }}
                    >
                      Cerrar Conteo
                    </button>
                  )}
                </div>
              ))}
            </div>
          )}
        </div>

        {selectedCount && countDetails && (
          <div className="bg-white rounded-lg shadow-md p-6 space-y-6">
            <h3 className="text-xl font-bold text-gray-800">Detalle del Conteo: {countDetails.name}</h3>
            
            {countDetails.status !== 'closed' && (
              <div className="bg-gradient-to-br from-purple-50 to-indigo-50 rounded-lg p-4 border border-purple-200">
                <h4 className="font-bold text-gray-800 mb-4">Agregar Item al Conteo</h4>
                <form onSubmit={handleAddItem} className="space-y-4">
                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-2">Producto *</label>
                    <select
                      value={itemForm.product_id}
                      onChange={(e) => setItemForm({ ...itemForm, product_id: e.target.value })}
                      required
                      className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-purple-500 focus:border-transparent bg-white"
                    >
                      <option value="">Selecciona un producto</option>
                      {products.map(p => (
                        <option key={p.id} value={p.id}>
                          {p.name} - {p.packaging_unit || 'Unidad'} (${p.price})
                        </option>
                      ))}
                    </select>
                  </div>
                  
                  {getSelectedProduct() && (
                    <div className="bg-white rounded-lg p-3 text-sm space-y-1">
                      <p><strong className="text-gray-700">Unidad de empaque:</strong> <span className="text-gray-600">{getSelectedProduct().packaging_unit || 'Unidad'}</span></p>
                      <p><strong className="text-gray-700">Unidades por empaque:</strong> <span className="text-gray-600">{getSelectedProduct().units_per_package || 1}</span></p>
                    </div>
                  )}
                  
                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-2">Cantidad de Empaques *</label>
                    <input
                      type="number"
                      min="1"
                      value={itemForm.packages_count}
                      onChange={(e) => setItemForm({ ...itemForm, packages_count: parseInt(e.target.value) })}
                      required
                      className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-purple-500 focus:border-transparent"
                    />
                  </div>
                  
                  <div className="bg-purple-100 rounded-lg p-3 flex justify-between items-center">
                    <strong className="text-purple-900">Unidades Totales:</strong> 
                    <span className="text-2xl font-bold text-purple-700">{calculatedUnits}</span>
                  </div>
                  
                  <button 
                    type="submit" 
                    className="w-full px-6 py-2 bg-gradient-to-r from-indigo-500 to-purple-600 text-white rounded-lg font-semibold hover:shadow-lg transition-all disabled:opacity-50"
                    disabled={loading}
                  >
                    {loading ? 'Agregando...' : 'Agregar Item'}
                  </button>
                </form>
              </div>
            )}
            
            <div>
              <h4 className="font-bold text-gray-800 mb-3">Items del Conteo ({countDetails.items?.length || 0})</h4>
              {countDetails.items?.length === 0 ? (
                <p className="text-gray-500 italic">No hay items en este conteo</p>
              ) : (
                <div className="overflow-x-auto">
                  <table className="w-full border-collapse">
                    <thead>
                      <tr className="bg-gray-50">
                        <th className="px-4 py-2 text-left text-xs font-medium text-gray-500 uppercase border-b">Producto</th>
                        <th className="px-4 py-2 text-left text-xs font-medium text-gray-500 uppercase border-b">Empaques</th>
                        <th className="px-4 py-2 text-left text-xs font-medium text-gray-500 uppercase border-b">Unidades</th>
                        <th className="px-4 py-2 text-left text-xs font-medium text-gray-500 uppercase border-b">Fecha Registro</th>
                      </tr>
                    </thead>
                    <tbody className="bg-white divide-y divide-gray-200">
                      {countDetails.items?.map((item, index) => {
                        const product = products.find(p => p.id === item.product_id);
                        return (
                          <tr key={index} className="hover:bg-gray-50">
                            <td className="px-4 py-2 text-sm text-gray-900">{product?.name || `ID: ${item.product_id}`}</td>
                            <td className="px-4 py-2 text-sm text-gray-600">{item.packages_count}</td>
                            <td className="px-4 py-2 text-sm font-bold text-purple-600">{item.quantity}</td>
                            <td className="px-4 py-2 text-sm text-gray-600">{new Date(item.created_at).toLocaleString()}</td>
                          </tr>
                        );
                      })}
                    </tbody>
                  </table>
                </div>
              )}
            </div>
            
            {countDetails.closed_at && (
              <div className="bg-blue-50 border-l-4 border-blue-500 text-blue-700 p-3 rounded">
                <strong>Conteo cerrado el:</strong> {new Date(countDetails.closed_at).toLocaleString()}
              </div>
            )}
          </div>
        )}
      </div>
    </div>
  );
}

export default InventoryCount;
