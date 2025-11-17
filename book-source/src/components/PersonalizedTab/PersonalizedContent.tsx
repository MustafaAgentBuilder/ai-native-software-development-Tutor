// Claude is Work to Build this Project
/**
 * PersonalizedContent Component
 * Fetches and displays personalized lesson content
 */

import React, { useState, useEffect } from 'react';
import ReactMarkdown from 'react-markdown';
import apiClient, { PersonalizedContentResponse, UserProfile } from '../../services/api';
import styles from './styles.module.css';

interface PersonalizedContentProps {
  pagePath: string;
  user: UserProfile;
  onLogout: () => void;
}

export default function PersonalizedContent({ pagePath, user, onLogout }: PersonalizedContentProps): JSX.Element {
  const [content, setContent] = useState<PersonalizedContentResponse | null>(null);
  const [loading, setLoading] = useState<boolean>(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    loadPersonalizedContent();
  }, [pagePath]);

  const loadPersonalizedContent = async () => {
    setLoading(true);
    setError(null);

    try {
      const personalizedContent = await apiClient.getPersonalizedContent(pagePath);
      setContent(personalizedContent);
      setLoading(false);
    } catch (err) {
      console.error('Error loading personalized content:', err);
      setError(err instanceof Error ? err.message : 'Failed to load personalized content');
      setLoading(false);
    }
  };

  const handleRegenerate = async () => {
    // TODO: Add regenerate functionality (requires backend endpoint)
    // For now, just reload
    await loadPersonalizedContent();
  };

  if (loading) {
    return (
      <div className={styles.personalizedContainer}>
        <div className={styles.personalizedHeader}>
          <div className={styles.userInfo}>
            <span className={styles.userEmail}>👤 {user.email}</span>
            <button className={styles.logoutButton} onClick={onLogout}>
              Logout
            </button>
          </div>
        </div>

        <div className={styles.loadingState}>
          <div className={styles.spinner}></div>
          <h3>✨ OLIVIA is personalizing this lesson for you...</h3>
          <p>This may take 10-20 seconds</p>
          <div className={styles.profileSummary}>
            <p>
              <strong>Your Profile:</strong> {user.programming_experience} programmer,{' '}
              {user.ai_experience} AI experience, {user.learning_style} learning style
            </p>
          </div>
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div className={styles.personalizedContainer}>
        <div className={styles.personalizedHeader}>
          <div className={styles.userInfo}>
            <span className={styles.userEmail}>👤 {user.email}</span>
            <button className={styles.logoutButton} onClick={onLogout}>
              Logout
            </button>
          </div>
        </div>

        <div className={styles.errorState}>
          <h3>❌ Error Loading Content</h3>
          <p className={styles.errorMessage}>{error}</p>
          <button className={styles.retryButton} onClick={loadPersonalizedContent}>
            Try Again
          </button>
        </div>
      </div>
    );
  }

  if (!content) {
    return (
      <div className={styles.personalizedContainer}>
        <div className={styles.errorState}>
          <h3>⚠️ No Content Available</h3>
          <p>Unable to load personalized content</p>
        </div>
      </div>
    );
  }

  return (
    <div className={styles.personalizedContainer}>
      {/* Header with user info and logout */}
      <div className={styles.personalizedHeader}>
        <div className={styles.userInfo}>
          <span className={styles.userEmail}>👤 {user.email}</span>
          <button className={styles.logoutButton} onClick={onLogout}>
            Logout
          </button>
        </div>
      </div>

      {/* Cache status badge */}
      <div className={styles.contentMeta}>
        {content.cached ? (
          <span className={styles.badge + ' ' + styles.cachedBadge}>
            ⚡ Loaded from cache
          </span>
        ) : (
          <span className={styles.badge + ' ' + styles.freshBadge}>
            ✨ Freshly generated
          </span>
        )}
        <span className={styles.badge}>
          🤖 {content.model_version}
        </span>
        <span className={styles.badge}>
          📅 {new Date(content.generated_at).toLocaleDateString()}
        </span>
      </div>

      {/* Profile summary */}
      <div className={styles.profileBanner}>
        <div className={styles.profileBannerContent}>
          <h4>Personalized for Your Profile</h4>
          <div className={styles.profileTags}>
            <span className={styles.profileTag}>
              💻 {user.programming_experience}
            </span>
            <span className={styles.profileTag}>
              🤖 AI: {user.ai_experience}
            </span>
            <span className={styles.profileTag}>
              📚 {user.learning_style}
            </span>
            <span className={styles.profileTag}>
              🌐 {user.preferred_language}
            </span>
          </div>
        </div>
      </div>

      {/* Personalized content */}
      <div className={styles.markdownContent}>
        <ReactMarkdown>{content.markdown_content}</ReactMarkdown>
      </div>

      {/* Footer */}
      <div className={styles.contentFooter}>
        <p className={styles.footerText}>
          ✨ This lesson was personalized by <strong>OLIVIA AI Tutor</strong> based on your learning profile
        </p>
        {/* Future: Add regenerate button */}
        {/*
        <button className={styles.regenerateButton} onClick={handleRegenerate}>
          🔄 Regenerate Content
        </button>
        */}
      </div>
    </div>
  );
}
