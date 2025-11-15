import { writable } from 'svelte/store';
import { browser } from '$app/environment';

interface User {
  id: string;
  email: string;
  name: string;
  avatar?: string;
}

interface AuthState {
  user: User | null;
  token: string | null;
  isAuthenticated: boolean;
  loading: boolean;
}

const initialState: AuthState = {
  user: null,
  token: browser ? localStorage.getItem('auth_token') : null,
  isAuthenticated: false,
  loading: false,
};

function createAuthStore() {
  const { subscribe, set, update } = writable<AuthState>(initialState);

  return {
    subscribe,
    login: async (email: string, password: string) => {
      update(state => ({ ...state, loading: true }));
      
      try {
        const response = await fetch('http://localhost:8000/api/auth/login/', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ email, password }),
        });

        if (!response.ok) throw new Error('Login failed');

        const data = await response.json();
        
        if (browser) {
          localStorage.setItem('auth_token', data.token);
        }

        update(state => ({
          ...state,
          user: data.user,
          token: data.token,
          isAuthenticated: true,
          loading: false,
        }));

        return data;
      } catch (error) {
        update(state => ({ ...state, loading: false }));
        throw error;
      }
    },
    
    signup: async (email: string, password: string, name: string) => {
      update(state => ({ ...state, loading: true }));
      
      try {
        const response = await fetch('http://localhost:8000/api/auth/signup/', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ email, password, name }),
        });

        if (!response.ok) throw new Error('Signup failed');

        const data = await response.json();
        
        if (browser) {
          localStorage.setItem('auth_token', data.token);
        }

        update(state => ({
          ...state,
          user: data.user,
          token: data.token,
          isAuthenticated: true,
          loading: false,
        }));

        return data;
      } catch (error) {
        update(state => ({ ...state, loading: false }));
        throw error;
      }
    },
    
    logout: () => {
      if (browser) {
        localStorage.removeItem('auth_token');
      }
      set(initialState);
    },
    
    checkAuth: async () => {
      const token = browser ? localStorage.getItem('auth_token') : null;
      
      if (!token) return;

      try {
        const response = await fetch('http://localhost:8000/api/auth/me/', {
          headers: { 'Authorization': `Bearer ${token}` },
        });

        if (!response.ok) throw new Error('Auth check failed');

        const user = await response.json();
        
        update(state => ({
          ...state,
          user,
          token,
          isAuthenticated: true,
        }));
      } catch {
        if (browser) {
          localStorage.removeItem('auth_token');
        }
        set(initialState);
      }
    },
  };
}

export const authStore = createAuthStore();