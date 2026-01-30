import React, { useState, useEffect } from 'react';
import { useAuth } from './context/AuthContext';
import { Header, TabButton } from './components';
import { LoginView, UsersView, ProductsView, WarehousesView, InventoryCountView } from './views';

function App() {
  const { isAuthenticated, user, loading } = useAuth();
  const [activeTab, setActiveTab] = useState('counts');
  
  const isAdmin = user?.role === 'admin';

  // Actualizar pestaña activa cuando el usuario se carga
  useEffect(() => {
    if (user) {
      console.log('User loaded:', user); // Debug: verificar datos del usuario
      console.log('User role:', user.role); // Debug: verificar rol específico
      console.log('Is admin?:', user.role === 'admin'); // Debug: verificar comparación
      setActiveTab(user.role === 'admin' ? 'users' : 'counts');
    }
  }, [user]);

  if (loading) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-purple-600"></div>
      </div>
    );
  }

  if (!isAuthenticated) {
    return <LoginView />;
  }

  return (
    <div className="flex flex-col min-h-screen bg-gray-100">
      <header className="bg-gradient-to-r from-indigo-500 via-purple-500 to-purple-600 text-white shadow-lg relative">
        <Header />
        <nav className="flex gap-2 px-8">
          {/* Solo ADMIN puede ver estas pestañas */}
          {isAdmin && (
            <>
              <TabButton
                active={activeTab === 'users'}
                onClick={() => setActiveTab('users')}
              >
                Usuarios
              </TabButton>
              <TabButton
                active={activeTab === 'products'}
                onClick={() => setActiveTab('products')}
              >
                Productos
              </TabButton>
              <TabButton
                active={activeTab === 'warehouses'}
                onClick={() => setActiveTab('warehouses')}
              >
                Bodegas
              </TabButton>
            </>
          )}
          {/* Todos los usuarios pueden ver conteos */}
          <TabButton
            active={activeTab === 'counts'}
            onClick={() => setActiveTab('counts')}
          >
            Conteos de Inventario
          </TabButton>
        </nav>
      </header>

      <main className="flex-1 p-8">
        {/* Protección de acceso: USER solo puede ver conteos */}
        {isAdmin && activeTab === 'users' && <UsersView userRole={user?.role} />}
        {isAdmin && activeTab === 'products' && <ProductsView userRole={user?.role} />}
        {isAdmin && activeTab === 'warehouses' && <WarehousesView userRole={user?.role} />}
        {activeTab === 'counts' && <InventoryCountView token={null} userRole={user?.role} />}
        
        {/* Mensaje si un USER intenta acceder a pestañas restringidas */}
        {!isAdmin && ['users', 'products', 'warehouses'].includes(activeTab) && (
          <div className="bg-red-50 border-l-4 border-red-500 p-6 rounded-lg">
            <h3 className="text-red-800 font-bold text-lg mb-2">⛔ Acceso Denegado</h3>
            <p className="text-red-700">No tienes permisos para acceder a esta sección. Los usuarios solo pueden acceder a Conteos de Inventario.</p>
          </div>
        )}
      </main>
    </div>
  );
}

export default App;
