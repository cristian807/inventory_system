import React from 'react';
import { useAuth } from '../context/AuthContext';

function Header() {
  const { user, logout } = useAuth();

  return (
    <div className="px-8 pt-8 pb-6">
      <h1 className="text-4xl font-bold mb-6">Sistema de Inventario</h1>
      <div className="absolute top-4 right-8 flex items-center gap-4 bg-white/10 backdrop-blur-md px-4 py-2 rounded-lg">
        <span className="text-sm opacity-95">
          Bienvenido, <strong>{user?.username}</strong>
        </span>
        <span className="text-xs bg-white/20 px-3 py-1 rounded-full">
          Rol: {user?.role}
        </span>
        <button 
          onClick={logout}
          className="text-sm bg-white/20 hover:bg-white/30 px-4 py-1.5 rounded-lg transition-all hover:scale-105"
        >
          Cerrar Sesión
        </button>
      </div>
    </div>
  );
}

export default Header;
