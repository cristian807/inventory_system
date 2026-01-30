import React from 'react';

function TabButton({ active, onClick, children, count }) {
  return (
    <button
      className={`px-6 py-3 rounded-t-lg font-medium transition-all ${
        active
          ? 'bg-white text-purple-600 shadow-lg'
          : 'bg-white/10 text-white hover:bg-white/20'
      }`}
      onClick={onClick}
    >
      {children}
      {count !== undefined && ` (${count})`}
    </button>
  );
}

export default TabButton;
