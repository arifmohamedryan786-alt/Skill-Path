import React, { createContext, useContext, useState } from 'react';
import { CheckCircle2, AlertCircle, Info, X } from 'lucide-react';

interface Toast {
  id: string;
  type: 'success' | 'warning' | 'error' | 'info';
  message: string;
}

interface ToastContextType {
  showToast: (message: string, type?: 'success' | 'warning' | 'error' | 'info') => void;
  addToast: (message: string, type?: 'success' | 'warning' | 'error' | 'info') => void;
}

const ToastContext = createContext<ToastContextType | undefined>(undefined);

export const ToastProvider: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  const [toasts, setToasts] = useState<Toast[]>([]);

  const showToast = (message: string, type: 'success' | 'warning' | 'error' | 'info' = 'success') => {
    const id = Math.random().toString(36).substring(2, 9);
    setToasts((prev) => [...prev, { id, type, message }]);
    setTimeout(() => {
      setToasts((prev) => prev.filter((t) => t.id !== id));
    }, 4500);
  };

  const removeToast = (id: string) => {
    setToasts((prev) => prev.filter((t) => t.id !== id));
  };

  return (
    <ToastContext.Provider value={{ showToast, addToast: showToast }}>
      {children}
      <div className="fixed bottom-5 right-5 z-50 flex flex-col gap-2 max-w-sm w-full pointer-events-none">
        {toasts.map((toast) => (
          <div
            key={toast.id}
            className={`pointer-events-auto flex items-start gap-3 p-3.5 rounded-md border shadow-card transition-all duration-200 bg-surface ${
              toast.type === 'success'
                ? 'border-status-success/30 text-ink'
                : toast.type === 'warning'
                ? 'border-status-warning/30 text-ink'
                : toast.type === 'error'
                ? 'border-status-danger/30 text-ink'
                : 'border-primary/30 text-ink'
            }`}
          >
            {toast.type === 'success' && <CheckCircle2 className="w-5 h-5 text-status-success shrink-0 mt-0.5" />}
            {toast.type === 'warning' && <AlertCircle className="w-5 h-5 text-status-warning shrink-0 mt-0.5" />}
            {toast.type === 'error' && <AlertCircle className="w-5 h-5 text-status-danger shrink-0 mt-0.5" />}
            {toast.type === 'info' && <Info className="w-5 h-5 text-primary shrink-0 mt-0.5" />}

            <div className="text-sm font-medium leading-snug flex-1">{toast.message}</div>
            <button
              onClick={() => removeToast(toast.id)}
              className="text-ink-secondary hover:text-ink shrink-0 p-0.5"
            >
              <X className="w-4 h-4" />
            </button>
          </div>
        ))}
      </div>
    </ToastContext.Provider>
  );
};

export function useToast() {
  const context = useContext(ToastContext);
  if (!context) throw new Error('useToast must be used within a ToastProvider');
  return context;
}
