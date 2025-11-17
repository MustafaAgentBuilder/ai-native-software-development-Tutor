// Claude is Work to Build this Project
/**
 * PersonalizedTab Component
 * Main component for personalized content tab
 * Handles auth state and shows login/signup or personalized content
 */

import React, { useState } from 'react';
import { useAuth } from '../../hooks/useAuth';
import { SignupRequest, LoginRequest } from '../../services/api';
import LoginForm from './LoginForm';
import SignupForm from './SignupForm';
import PersonalizedContent from './PersonalizedContent';
import styles from './styles.module.css';

interface PersonalizedTabProps {
  /** Current page path from Docusaurus (e.g., "01-Introducing-AI-Driven-Development/01-ai-development-revolution/01-moment_that_changed_everything") */
  pagePath: string;
}

export default function PersonalizedTab({ pagePath }: PersonalizedTabProps): JSX.Element {
  const { isAuthenticated, user, loading, error, signup, login, logout, clearError } = useAuth();
  const [showSignup, setShowSignup] = useState(false);

  const handleSignup = async (data: SignupRequest) => {
    try {
      await signup(data);
      // Success - user is now authenticated
    } catch (err) {
      // Error is handled by useAuth and available in error state
      console.error('Signup error:', err);
    }
  };

  const handleLogin = async (email: string, password: string) => {
    const loginData: LoginRequest = { email, password };
    try {
      await login(loginData);
      // Success - user is now authenticated
    } catch (err) {
      // Error is handled by useAuth and available in error state
      console.error('Login error:', err);
    }
  };

  const handleLogout = async () => {
    await logout();
    setShowSignup(false);
  };

  const switchToSignup = () => {
    clearError();
    setShowSignup(true);
  };

  const switchToLogin = () => {
    clearError();
    setShowSignup(false);
  };

  // Show loading state while checking auth
  if (loading && !isAuthenticated) {
    return (
      <div className={styles.container}>
        <div className={styles.loadingState}>
          <div className={styles.spinner}></div>
          <p>Loading...</p>
        </div>
      </div>
    );
  }

  // User is authenticated - show personalized content
  if (isAuthenticated && user) {
    return (
      <div className={styles.container}>
        <PersonalizedContent
          pagePath={pagePath}
          user={user}
          onLogout={handleLogout}
        />
      </div>
    );
  }

  // User is NOT authenticated - show login or signup form
  return (
    <div className={styles.container}>
      {showSignup ? (
        <SignupForm
          onSignup={handleSignup}
          onSwitchToLogin={switchToLogin}
          error={error}
          loading={loading}
        />
      ) : (
        <LoginForm
          onLogin={handleLogin}
          onSwitchToSignup={switchToSignup}
          error={error}
          loading={loading}
        />
      )}
    </div>
  );
}
