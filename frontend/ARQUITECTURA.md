# 📁 Arquitectura Frontend - Sistema de Inventario

## 🏗️ Estructura de Carpetas

```
frontend/src/
├── components/          # Componentes reutilizables
│   ├── Button.jsx       # Botón personalizado con variantes
│   ├── ErrorAlert.jsx   # Alerta de errores
│   ├── Header.jsx       # Encabezado de la aplicación
│   ├── LoadingSpinner.jsx # Indicador de carga
│   ├── Modal.jsx        # Modal genérico
│   ├── Table.jsx        # Tabla genérica con acciones
│   ├── TabButton.jsx    # Botón de navegación
│   └── index.js         # Exportaciones centralizadas
│
├── context/             # Contextos de React
│   └── AuthContext.jsx  # Contexto de autenticación global
│
├── hooks/               # Custom hooks
│   ├── useApi.js        # Hook para llamadas API
│   ├── useModal.js      # Hook para modales
│   └── index.js         # Exportaciones centralizadas
│
├── services/            # Servicios de API
│   ├── apiClient.js     # Cliente Axios configurado
│   ├── authService.js   # Servicios de autenticación
│   ├── inventoryService.js # Servicios de inventario
│   ├── productService.js   # Servicios de productos
│   ├── userService.js      # Servicios de usuarios
│   ├── warehouseService.js # Servicios de bodegas
│   └── index.js         # Exportaciones centralizadas
│
├── views/               # Vistas/Páginas principales
│   ├── InventoryCountView.jsx # Gestión de conteos
│   ├── LoginView.jsx          # Login y registro
│   ├── ProductsView.jsx       # CRUD de productos
│   ├── UsersView.jsx          # CRUD de usuarios
│   ├── WarehousesView.jsx     # CRUD de bodegas
│   └── index.js               # Exportaciones centralizadas
│
├── App.jsx              # Componente principal
├── main.jsx             # Punto de entrada
└── index.css            # Estilos globales (Tailwind)
```

---

## 🎯 Principios de Arquitectura

### 1. **Separación de Responsabilidades**
- **Components**: Componentes UI reutilizables sin lógica de negocio
- **Views**: Páginas completas con lógica específica
- **Services**: Lógica de comunicación con API
- **Hooks**: Lógica reutilizable y estado personalizado
- **Context**: Estado global de la aplicación

### 2. **Reutilización de Código**
- Componentes genéricos (Modal, Table, Button)
- Hooks personalizados (useApi, useModal)
- Servicios modulares por entidad

### 3. **Escalabilidad**
- Estructura clara para agregar nuevas funcionalidades
- Importaciones centralizadas con `index.js`
- Separación clara entre UI y lógica

---

## 📦 Componentes Reutilizables

### Button
```jsx
import { Button } from './components';

<Button variant="primary" onClick={handleClick}>
  Click Me
</Button>

// Variantes: primary, secondary, danger, success
```

### Modal
```jsx
import { Modal } from './components';

<Modal isOpen={isOpen} onClose={handleClose} title="Mi Modal" size="md">
  {/* Contenido del modal */}
</Modal>

// Tamaños: sm, md, lg, xl, 2xl
```

### Table
```jsx
import { Table } from './components';

const columns = [
  { header: 'ID', key: 'id' },
  { header: 'Nombre', key: 'name' },
  { 
    header: 'Estado', 
    render: (row) => <span>{row.status}</span> 
  }
];

<Table 
  columns={columns} 
  data={users} 
  onEdit={handleEdit}
  onDelete={handleDelete}
/>
```

### ErrorAlert
```jsx
import { ErrorAlert } from './components';

<ErrorAlert message={error} onClose={() => setError(null)} />
```

### LoadingSpinner
```jsx
import { LoadingSpinner } from './components';

<LoadingSpinner message="Cargando datos..." />
```

---

## 🎣 Custom Hooks

### useApi
```jsx
import { useApi } from './hooks';
import { userService } from './services';

const { data, loading, error, execute } = useApi(userService.getAll);

// Ejecutar la llamada
useEffect(() => {
  execute(0, 100);
}, []);
```

### useModal
```jsx
import { useModal } from './hooks';

const { isOpen, open, close, toggle } = useModal();

<button onClick={open}>Abrir Modal</button>
<Modal isOpen={isOpen} onClose={close}>...</Modal>
```

---

## 🌐 Servicios API

### Estructura de Servicios
Cada servicio exporta métodos CRUD estándar:

```jsx
import { userService } from './services';

// GET All
const users = await userService.getAll(skip, limit);

// GET By ID
const user = await userService.getById(id);

// POST Create
const newUser = await userService.create(userData);

// PUT Update
const updated = await userService.update(id, userData);

// DELETE
await userService.delete(id);
```

### Configuración de Token
```jsx
import { setAuthToken } from './services';

// Configurar token para todas las peticiones
setAuthToken(token);

// Limpiar token
setAuthToken(null);
```

---

## 🔐 Context de Autenticación

### AuthContext
Provee estado global de autenticación:

```jsx
import { useAuth } from './context/AuthContext';

function MyComponent() {
  const { isAuthenticated, user, token, loading, login, logout } = useAuth();

  // user = { username: '...', role: 'ADMIN' | 'USER' }
  
  return (
    <div>
      {isAuthenticated ? (
        <p>Bienvenido {user.username}</p>
      ) : (
        <p>Inicia sesión</p>
      )}
    </div>
  );
}
```

---

## 📄 Vistas Principales

### LoginView
- Login y registro de usuarios
- Manejo de sesión con localStorage
- Integración con AuthContext

### UsersView (ADMIN only)
- CRUD completo de usuarios
- Asignación de bodegas
- Gestión de roles

### ProductsView
- CRUD completo de productos
- Gestión de unidades de empaque
- Solo ADMIN puede modificar

### WarehousesView
- CRUD completo de bodegas
- Vista de cards responsive
- Solo ADMIN puede modificar

### InventoryCountView
- Creación de conteos de inventario
- Registro de items con cálculo automático
- Filtros por bodega y estado
- Permisos según rol

---

## 🚀 Flujo de Trabajo

### 1. Agregar Nueva Vista
```bash
# Crear archivo en views/
touch src/views/MyNewView.jsx

# Exportar en views/index.js
export { default as MyNewView } from './MyNewView';

# Importar en App.jsx
import { MyNewView } from './views';
```

### 2. Agregar Nuevo Servicio
```bash
# Crear archivo en services/
touch src/services/myService.js

# Exportar en services/index.js
export { myService } from './myService';
```

### 3. Agregar Nuevo Componente
```bash
# Crear archivo en components/
touch src/components/MyComponent.jsx

# Exportar en components/index.js
export { default as MyComponent } from './MyComponent';
```

### 4. Agregar Nuevo Hook
```bash
# Crear archivo en hooks/
touch src/hooks/useMyHook.js

# Exportar en hooks/index.js
export { useMyHook } from './useMyHook';
```

---

## 💡 Buenas Prácticas

### Imports
```jsx
// ✅ CORRECTO - Importaciones organizadas
import React, { useState, useEffect } from 'react';
import { userService } from '../services';
import { Button, Modal } from '../components';
import { useApi, useModal } from '../hooks';

// ❌ INCORRECTO - Importaciones relativas largas
import Button from '../../components/Button';
import userService from '../../services/userService';
```

### Componentes
```jsx
// ✅ CORRECTO - Componente pequeño y enfocado
function UserCard({ user, onEdit }) {
  return (
    <div className="card">
      <h3>{user.name}</h3>
      <Button onClick={() => onEdit(user)}>Editar</Button>
    </div>
  );
}

// ❌ INCORRECTO - Componente con demasiada lógica
function UserCard({ user }) {
  const [loading, setLoading] = useState(false);
  const [editing, setEditing] = useState(false);
  // ... mucha lógica
}
```

### Estado
```jsx
// ✅ CORRECTO - useAuth para autenticación
const { user, isAuthenticated } = useAuth();

// ❌ INCORRECTO - localStorage directo en componentes
const user = JSON.parse(localStorage.getItem('userData'));
```

---

## 🔧 Configuración

### Variables de Entorno
```bash
# .env
VITE_API_URL=http://localhost:8000/api
```

### Tailwind CSS
- Configuración en `tailwind.config.js`
- Colores personalizados (indigo, purple)
- Estilos globales en `index.css`

---

## 📊 Beneficios de Esta Arquitectura

✅ **Mantenibilidad**: Código organizado y fácil de encontrar
✅ **Escalabilidad**: Agregar nuevas funcionalidades sin modificar código existente
✅ **Reutilización**: Componentes y lógica compartida
✅ **Testabilidad**: Servicios y hooks fáciles de probar
✅ **Separación de Responsabilidades**: UI, lógica y datos separados
✅ **Legibilidad**: Estructura clara y consistente
✅ **Performance**: Importaciones optimizadas con tree-shaking

---

## 📝 Notas Importantes

- Todos los archivos `index.js` son para **centralizar exportaciones**
- Los servicios **siempre** usan `apiClient` configurado
- El token se configura **globalmente** en axios, no por petición
- Los componentes de `components/` **no deben** tener lógica de negocio
- Las vistas en `views/` pueden tener lógica específica de la página
- El contexto `AuthContext` **debe** envolver toda la aplicación

---

## 🎨 Stack Tecnológico

- **React 18** - Biblioteca UI
- **Vite 5.4** - Build tool
- **Axios** - Cliente HTTP
- **Tailwind CSS 3.3** - Framework CSS
- **Context API** - Gestión de estado global
- **Custom Hooks** - Lógica reutilizable

---

Desarrollado con ❤️ para un sistema de inventario escalable y mantenible.
