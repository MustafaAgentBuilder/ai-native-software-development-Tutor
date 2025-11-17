// Claude is Work to Build this Project
/**
 * SignupForm Component
 * New user registration with 4 profile questions
 */

import React, { useState } from 'react';
import { SignupRequest } from '../../services/api';
import styles from './styles.module.css';

interface SignupFormProps {
  onSignup: (data: SignupRequest) => Promise<void>;
  onSwitchToLogin: () => void;
  error?: string | null;
  loading?: boolean;
}

export default function SignupForm({ onSignup, onSwitchToLogin, error, loading }: SignupFormProps): JSX.Element {
  const [formData, setFormData] = useState<SignupRequest>({
    email: '',
    password: '',
    programming_experience: 'beginner',
    ai_experience: 'none',
    learning_style: 'mixed',
    preferred_language: 'en',
    full_name: '',
  });

  const [confirmPassword, setConfirmPassword] = useState('');
  const [validationError, setValidationError] = useState<string | null>(null);

  const handleInputChange = (e: React.ChangeEvent<HTMLInputElement | HTMLSelectElement>) => {
    const { name, value } = e.target;
    setFormData((prev) => ({ ...prev, [name]: value }));
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setValidationError(null);

    // Validation
    if (!formData.email || !formData.password) {
      setValidationError('Email and password are required');
      return;
    }

    if (!formData.email.includes('@')) {
      setValidationError('Please enter a valid email address');
      return;
    }

    if (formData.password.length < 8) {
      setValidationError('Password must be at least 8 characters long');
      return;
    }

    if (formData.password !== confirmPassword) {
      setValidationError('Passwords do not match');
      return;
    }

    try {
      await onSignup(formData);
    } catch (err) {
      // Error handled by parent component
    }
  };

  return (
    <div className={styles.authForm}>
      <div className={styles.authHeader}>
        <h2>🚀 Create Your Learning Profile</h2>
        <p>Help OLIVIA personalize your learning experience</p>
      </div>

      <form onSubmit={handleSubmit} className={styles.form}>
        {/* Error messages */}
        {(error || validationError) && (
          <div className={styles.errorMessage}>
            {error || validationError}
          </div>
        )}

        {/* Basic Info Section */}
        <div className={styles.formSection}>
          <h3>Basic Information</h3>

          <div className={styles.formGroup}>
            <label htmlFor="full_name" className={styles.label}>
              Full Name (Optional)
            </label>
            <input
              type="text"
              id="full_name"
              name="full_name"
              className={styles.input}
              placeholder="Your name"
              value={formData.full_name}
              onChange={handleInputChange}
              disabled={loading}
            />
          </div>

          <div className={styles.formGroup}>
            <label htmlFor="email" className={styles.label}>
              Email Address *
            </label>
            <input
              type="email"
              id="email"
              name="email"
              className={styles.input}
              placeholder="your.email@example.com"
              value={formData.email}
              onChange={handleInputChange}
              disabled={loading}
              required
            />
          </div>

          <div className={styles.formGroup}>
            <label htmlFor="password" className={styles.label}>
              Password * (min 8 characters)
            </label>
            <input
              type="password"
              id="password"
              name="password"
              className={styles.input}
              placeholder="Create a secure password"
              value={formData.password}
              onChange={handleInputChange}
              disabled={loading}
              required
              minLength={8}
            />
          </div>

          <div className={styles.formGroup}>
            <label htmlFor="confirmPassword" className={styles.label}>
              Confirm Password *
            </label>
            <input
              type="password"
              id="confirmPassword"
              className={styles.input}
              placeholder="Re-enter your password"
              value={confirmPassword}
              onChange={(e) => setConfirmPassword(e.target.value)}
              disabled={loading}
              required
            />
          </div>
        </div>

        {/* Profile Questions Section */}
        <div className={styles.formSection}>
          <h3>Learning Profile (4 Questions)</h3>
          <p className={styles.sectionDescription}>
            These questions help OLIVIA adapt content to your level and style
          </p>

          {/* Question 1: Programming Experience */}
          <div className={styles.formGroup}>
            <label className={styles.label}>
              1. Programming Experience *
            </label>
            <div className={styles.radioGroup}>
              <label className={styles.radioLabel}>
                <input
                  type="radio"
                  name="programming_experience"
                  value="beginner"
                  checked={formData.programming_experience === 'beginner'}
                  onChange={handleInputChange}
                  disabled={loading}
                />
                <span>Beginner (&lt; 6 months)</span>
              </label>
              <label className={styles.radioLabel}>
                <input
                  type="radio"
                  name="programming_experience"
                  value="intermediate"
                  checked={formData.programming_experience === 'intermediate'}
                  onChange={handleInputChange}
                  disabled={loading}
                />
                <span>Intermediate (6 months - 2 years)</span>
              </label>
              <label className={styles.radioLabel}>
                <input
                  type="radio"
                  name="programming_experience"
                  value="advanced"
                  checked={formData.programming_experience === 'advanced'}
                  onChange={handleInputChange}
                  disabled={loading}
                />
                <span>Advanced (2+ years)</span>
              </label>
            </div>
          </div>

          {/* Question 2: AI/ML Experience */}
          <div className={styles.formGroup}>
            <label className={styles.label}>
              2. AI/ML Experience *
            </label>
            <div className={styles.radioGroup}>
              <label className={styles.radioLabel}>
                <input
                  type="radio"
                  name="ai_experience"
                  value="none"
                  checked={formData.ai_experience === 'none'}
                  onChange={handleInputChange}
                  disabled={loading}
                />
                <span>No experience with AI</span>
              </label>
              <label className={styles.radioLabel}>
                <input
                  type="radio"
                  name="ai_experience"
                  value="basic"
                  checked={formData.ai_experience === 'basic'}
                  onChange={handleInputChange}
                  disabled={loading}
                />
                <span>Used AI tools but not built with them</span>
              </label>
              <label className={styles.radioLabel}>
                <input
                  type="radio"
                  name="ai_experience"
                  value="intermediate"
                  checked={formData.ai_experience === 'intermediate'}
                  onChange={handleInputChange}
                  disabled={loading}
                />
                <span>Built some AI projects</span>
              </label>
              <label className={styles.radioLabel}>
                <input
                  type="radio"
                  name="ai_experience"
                  value="advanced"
                  checked={formData.ai_experience === 'advanced'}
                  onChange={handleInputChange}
                  disabled={loading}
                />
                <span>Regular AI/ML development</span>
              </label>
            </div>
          </div>

          {/* Question 3: Learning Style */}
          <div className={styles.formGroup}>
            <label className={styles.label}>
              3. Learning Style Preference *
            </label>
            <div className={styles.radioGroup}>
              <label className={styles.radioLabel}>
                <input
                  type="radio"
                  name="learning_style"
                  value="visual"
                  checked={formData.learning_style === 'visual'}
                  onChange={handleInputChange}
                  disabled={loading}
                />
                <span>Visual (diagrams, charts)</span>
              </label>
              <label className={styles.radioLabel}>
                <input
                  type="radio"
                  name="learning_style"
                  value="practical"
                  checked={formData.learning_style === 'practical'}
                  onChange={handleInputChange}
                  disabled={loading}
                />
                <span>Practical (code examples, hands-on)</span>
              </label>
              <label className={styles.radioLabel}>
                <input
                  type="radio"
                  name="learning_style"
                  value="conceptual"
                  checked={formData.learning_style === 'conceptual'}
                  onChange={handleInputChange}
                  disabled={loading}
                />
                <span>Conceptual (theory-first)</span>
              </label>
              <label className={styles.radioLabel}>
                <input
                  type="radio"
                  name="learning_style"
                  value="mixed"
                  checked={formData.learning_style === 'mixed'}
                  onChange={handleInputChange}
                  disabled={loading}
                />
                <span>Mixed (all approaches)</span>
              </label>
            </div>
          </div>

          {/* Question 4: Preferred Language */}
          <div className={styles.formGroup}>
            <label htmlFor="preferred_language" className={styles.label}>
              4. Preferred Language *
            </label>
            <select
              id="preferred_language"
              name="preferred_language"
              className={styles.select}
              value={formData.preferred_language}
              onChange={handleInputChange}
              disabled={loading}
              required
            >
              <option value="en">English</option>
              <option value="es">Spanish</option>
              <option value="fr">French</option>
              <option value="de">German</option>
              <option value="zh">Chinese</option>
              <option value="ja">Japanese</option>
            </select>
          </div>
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
              Creating account...
            </>
          ) : (
            'Create Account'
          )}
        </button>

        {/* Switch to login */}
        <div className={styles.switchForm}>
          <p>
            Already have an account?{' '}
            <button
              type="button"
              className={styles.linkButton}
              onClick={onSwitchToLogin}
              disabled={loading}
            >
              Log in
            </button>
          </p>
        </div>
      </form>
    </div>
  );
}
