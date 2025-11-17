// Claude is Work to Build this Project
/**
 * LoginForm Component
 * Email + Password login form
 */

import React, { useState } from 'react';
import styles from './styles.module.css';

interface LoginFormProps {
  onLogin: (email: string, password: string) => Promise<void>;
  onSwitchToSignup: () => void;
  error?: string | null;
  loading?: boolean;
}

export default function LoginForm({ onLogin, onSwitchToSignup, error, loading }: LoginFormProps): JSX.Element {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [validationError, setValidationError] = useState<string | null>(null);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setValidationError(null);

    // Validation
    if (!email || !password) {
      setValidationError('Please fill in all fields');
      return;
    }

    if (!email.includes('@')) {
      setValidationError('Please enter a valid email address');
      return;
    }

    try {
      await onLogin(email, password);
    } catch (err) {
      // Error handled by parent component
    }
  };

  return (
    <div className={styles.authForm}>
      <div className={styles.authHeader}>
        <h2>✨ Welcome Back!</h2>
        <p>Log in to continue your personalized learning journey</p>
      </div>

      <form onSubmit={handleSubmit} className={styles.form}>
        {/* Error messages */}
        {(error || validationError) && (
          <div className={styles.errorMessage}>
            {error || validationError}
          </div>
        )}

        {/* Email input */}
        <div className={styles.formGroup}>
          <label htmlFor="email" className={styles.label}>
            Email Address
          </label>
          <input
            type="email"
            id="email"
            className={styles.input}
            placeholder="your.email@example.com"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
            disabled={loading}
            required
          />
        </div>

        {/* Password input */}
        <div className={styles.formGroup}>
          <label htmlFor="password" className={styles.label}>
            Password
          </label>
          <input
            type="password"
            id="password"
            className={styles.input}
            placeholder="Enter your password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            disabled={loading}
            required
          />
        </div>

        {/* Submit button */}
        <button
          type="submit"
          className={styles.submitButton}
          disabled={loading}
        >
          {loading ? (
            <>
              <span className={styles.spinner}></span>
              Logging in...
            </>
          ) : (
            'Log In'
          )}
        </button>

        {/* Switch to signup */}
        <div className={styles.switchForm}>
          <p>
            Don't have an account?{' '}
            <button
              type="button"
              className={styles.linkButton}
              onClick={onSwitchToSignup}
              disabled={loading}
            >
              Sign up
            </button>
          </p>
        </div>
      </form>
    </div>
  );
}
