// Claude is Work to Build this Project
/**
 * useAuth Hook
 * Manages authentication state and provides auth methods
 */

import { useState, useEffect, useCallback } from 'react';
import apiClient, { UserProfile, SignupRequest, LoginRequest } from '../services/api';

interface AuthState {
  isAuthenticated: boolean;
  user: UserProfile | null;
  loading: boolean;
  error: string | null;
}

interface UseAuthReturn extends AuthState {
  signup: (data: SignupRequest) => Promise<void>;
  login: (data: LoginRequest) => Promise<void>;
  logout: () => Promise<void>;
  clearError: () => void;
  refreshUser: () => Promise<void>;
}

export function useAuth(): UseAuthReturn {
  const [state, setState] = useState<AuthState>({
    isAuthenticated: false,
    user: null,
    loading: true,
    error: null,
  });

  /**
   * Initialize auth state on mount
   */
  useEffect(() => {
    initializeAuth();
  }, []);

  /**
   * Initialize authentication state
   * Check if token exists and validate it
   */
  const initializeAuth = async () => {
    try {
      // Check if token exists in localStorage
      if (!apiClient.isAuthenticated()) {
        setState({
          isAuthenticated: false,
          user: null,
          loading: false,
          error: null,
        });
        return;
      }

      // Validate token by fetching user profile
      const user = await apiClient.getCurrentUser();

      setState({
        isAuthenticated: true,
        user,
        loading: false,
        error: null,
      });
    } catch (error) {
      // Token invalid or expired
      apiClient.clearAuth();
      setState({
        isAuthenticated: false,
        user: null,
        loading: false,
        error: null,
      });
    }
  };

  /**
   * Sign up a new user
   */
  const signup = useCallback(async (data: SignupRequest) => {
    setState((prev) => ({ ...prev, loading: true, error: null }));

    try {
      const authData = await apiClient.signup(data);

      setState({
        isAuthenticated: true,
        user: authData.user,
        loading: false,
        error: null,
      });
    } catch (error) {
      setState((prev) => ({
        ...prev,
        loading: false,
        error: error instanceof Error ? error.message : 'Signup failed',
      }));
      throw error;
    }
  }, []);

  /**
   * Log in an existing user
   */
  const login = useCallback(async (data: LoginRequest) => {
    setState((prev) => ({ ...prev, loading: true, error: null }));

    try {
      const authData = await apiClient.login(data);

      setState({
        isAuthenticated: true,
        user: authData.user,
        loading: false,
        error: null,
      });
    } catch (error) {
      setState((prev) => ({
        ...prev,
        loading: false,
        error: error instanceof Error ? error.message : 'Login failed',
      }));
      throw error;
    }
  }, []);

  /**
   * Log out the current user
   */
  const logout = useCallback(async () => {
    await apiClient.logout();

    setState({
      isAuthenticated: false,
      user: null,
      loading: false,
      error: null,
    });
  }, []);

  /**
   * Clear error message
   */
  const clearError = useCallback(() => {
    setState((prev) => ({ ...prev, error: null }));
  }, []);

  /**
   * Refresh user profile
   */
  const refreshUser = useCallback(async () => {
    try {
      const user = await apiClient.getCurrentUser();
      setState((prev) => ({ ...prev, user }));
    } catch (error) {
      // Token invalid, log out
      await logout();
    }
  }, [logout]);

  return {
    ...state,
    signup,
    login,
    logout,
    clearError,
    refreshUser,
  };
}

export default useAuth;
