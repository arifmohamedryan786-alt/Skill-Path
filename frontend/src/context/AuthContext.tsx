import React, { createContext, useContext, useState, useEffect } from 'react';
import { User } from '../types';
import { api, setAuthToken, clearAuthToken, getAuthToken } from '../api/client';

interface AuthContextType {
  user: User | null;
  token: string | null;
  loading: boolean;
  login: (email: string, pass: string) => Promise<void>;
  register: (email: string, pass: string, name: string, role?: string) => Promise<void>;
  guestLogin: () => Promise<void>;
  logout: () => void;
  switchDemoUser: (personaOrEmail: string) => Promise<void>;
  refreshUser: () => Promise<void>;
}

const AuthContext = createContext<AuthContextType | undefined>(undefined);

export const AuthProvider: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  const [user, setUser] = useState<User | null>(null);
  const [token, setToken] = useState<string | null>(getAuthToken());
  const [loading, setLoading] = useState<boolean>(true);

  useEffect(() => {
    async function loadUser() {
      try {
        const currentToken = getAuthToken();
        const storedUser = localStorage.getItem('skillpath_user');

        if (!currentToken || !storedUser) {
          // Direct entry: automatically authenticate as primary learner without any credentials
          try {
            const res = await api.demoLogin('arif');
            setAuthToken(res.access_token);
            setToken(res.access_token);
            const defaultUser: User = {
              id: res.user_id || 1,
              email: res.email || 'arif@skillpath.dev',
              role: res.role || 'learner',
              full_name: res.full_name || 'Arif Mohamed',
              career_goal: res.career_goal || 'AI/ML Engineer',
              goal_status: res.goal_status || 'known',
            };
            setUser(defaultUser);
            localStorage.setItem('skillpath_user', JSON.stringify(defaultUser));
          } catch {
            const fallbackUser: User = {
              id: 1,
              email: 'arif@skillpath.dev',
              role: 'learner',
              full_name: 'Arif Mohamed',
              career_goal: 'AI/ML Engineer',
              goal_status: 'known',
            };
            setUser(fallbackUser);
            localStorage.setItem('skillpath_user', JSON.stringify(fallbackUser));
          }
        } else {
          setUser(JSON.parse(storedUser));
          setToken(currentToken);
        }
      } catch (err) {
        const fallbackUser: User = {
          id: 1,
          email: 'arif@skillpath.dev',
          role: 'learner',
          full_name: 'Arif Mohamed',
          career_goal: 'AI/ML Engineer',
          goal_status: 'known',
        };
        setUser(fallbackUser);
        localStorage.setItem('skillpath_user', JSON.stringify(fallbackUser));
      } finally {
        setLoading(false);
      }
    }
    loadUser();
  }, []);

  const login = async (email: string, pass: string) => {
    setLoading(true);
    try {
      const res = await api.login({ email, password: pass });
      setAuthToken(res.access_token);
      setToken(res.access_token);
      const userData: User = {
        id: res.user_id,
        email,
        role: res.role,
        full_name: res.full_name,
        career_goal: res.career_goal,
        goal_status: res.goal_status,
      };
      setUser(userData);
      localStorage.setItem('skillpath_user', JSON.stringify(userData));
    } finally {
      setLoading(false);
    }
  };

  const register = async (email: string, pass: string, name: string, role = 'learner') => {
    setLoading(true);
    try {
      const res = await api.register({ email, password: pass, full_name: name, role });
      setAuthToken(res.access_token);
      setToken(res.access_token);
      const userData: User = {
        id: res.user_id,
        email,
        role: res.role,
        full_name: res.full_name,
        career_goal: res.career_goal,
        goal_status: res.goal_status,
      };
      setUser(userData);
      localStorage.setItem('skillpath_user', JSON.stringify(userData));
    } finally {
      setLoading(false);
    }
  };

  const guestLogin = async () => {
    setLoading(true);
    try {
      const res = await api.guestLogin();
      setAuthToken(res.access_token);
      setToken(res.access_token);
      const userData: User = {
        id: res.user_id,
        email: res.email || `guest_${res.user_id}@guest.skillpath.dev`,
        role: res.role || 'learner',
        full_name: res.full_name || 'Guest Explorer',
        career_goal: res.career_goal,
        goal_status: res.goal_status || 'unknown',
      };
      setUser(userData);
      localStorage.setItem('skillpath_user', JSON.stringify(userData));
    } finally {
      setLoading(false);
    }
  };

  const logout = () => {
    clearAuthToken();
    const defaultUser: User = {
      id: 1,
      email: 'arif@skillpath.dev',
      role: 'learner',
      full_name: 'Arif Mohamed',
      career_goal: 'AI/ML Engineer',
      goal_status: 'known',
    };
    setUser(defaultUser);
    localStorage.setItem('skillpath_user', JSON.stringify(defaultUser));
    // Direct entry: ensure default user token is restored
    api.demoLogin('arif').then(res => {
      setAuthToken(res.access_token);
      setToken(res.access_token);
    }).catch(() => {});
  };

  const switchDemoUser = async (personaOrEmail: string) => {
    const cleanName = personaOrEmail.includes('@')
      ? personaOrEmail.split('@')[0]
      : personaOrEmail;
    setLoading(true);
    try {
      const res = await api.demoLogin(cleanName);
      setAuthToken(res.access_token);
      setToken(res.access_token);
      const userData: User = {
        id: res.user_id,
        email: res.email || `${cleanName}@skillpath.dev`,
        role: res.role,
        full_name: res.full_name,
        career_goal: res.career_goal,
        goal_status: res.goal_status,
      };
      setUser(userData);
      localStorage.setItem('skillpath_user', JSON.stringify(userData));
    } finally {
      setLoading(false);
    }
  };

  const refreshUser = async () => {
    try {
      const profile = await api.getProfile();
      if (user) {
        const updated: User = {
          ...user,
          full_name: profile.full_name || user.full_name,
          name: profile.full_name || user.full_name,
          career_goal: profile.career_goal || user.career_goal,
          goal_status: profile.goal_status || user.goal_status,
          profile: profile
        };
        setUser(updated);
        localStorage.setItem('skillpath_user', JSON.stringify(updated));
      }
    } catch {
      // ignore
    }
  };

  return (
    <AuthContext.Provider value={{ user, token, loading, login, register, guestLogin, logout, switchDemoUser, refreshUser }}>
      {children}
    </AuthContext.Provider>
  );
};

export function useAuth() {
  const context = useContext(AuthContext);
  if (!context) throw new Error('useAuth must be used within an AuthProvider');
  return context;
}
