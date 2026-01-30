import React, { createContext, useState, useEffect, useContext } from 'react';
import { setAuthToken } from '../services';

const AuthContext = createContext(null);

export const AuthProvider = ({ children }) => {
  const [isAuthenticated, setIsAuthenticated] = useState(false);
  const [user, setUser] = useState(null);
  const [token, setToken] = useState(null);
  const [loading, setLoading] = useState(true);

  // Verificar si hay sesión guardada al cargar
  useEffect(() => {
    const savedUserData = localStorage.getItem('userData');
    if (savedUserData) {
      try {
        const userData = JSON.parse(savedUserData);
        setToken(userData.token);
        setUser({
          username: userData.username,
          role: userData.role,
        });
        setIsAuthenticated(true);
        setAuthToken(userData.token);
      } catch (err) {
        localStorage.removeItem('userData');
      }
    }
    setLoading(false);
  }, []);

  const login = (userData) => {
    setToken(userData.token);
    setUser({
      username: userData.username,
      role: userData.role,
    });
    setIsAuthenticated(true);
    setAuthToken(userData.token);
  };

  const logout = () => {
    localStorage.removeItem('userData');
    setToken(null);
    setUser(null);
    setIsAuthenticated(false);
    setAuthToken(null);
  };

  const value = {
    isAuthenticated,
    user,
    token,
    loading,
    login,
    logout,
  };

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>;
};

export const useAuth = () => {
  const context = useContext(AuthContext);
  if (!context) {
    throw new Error('useAuth must be used within an AuthProvider');
  }
  return context;
};
