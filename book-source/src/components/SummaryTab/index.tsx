/**
 * SummaryTab Component
 *
 * Displays AI-generated summaries for book pages
 * - Loads summary from /summaries directory
 * - Shows "Team Working on it" for pages without summaries
 * - Integrates directly into Docusaurus pages
 */

import React, { useState, useEffect } from 'react';
import styles from './styles.module.css';

interface SummaryData {
  summary: string;
  keyConcepts: string[];
  metadata: {
    chapter: string;
    difficulty: string;
    read_time: string;
    generated: string;
  };
}

interface SummaryTabProps {
  /** Current page path from Docusaurus (e.g., "01-Introducing-AI-Driven-Development/01-ai-development-revolution/01-moment_that_changed_everything") */
  pagePath: string;
}

export default function SummaryTab({ pagePath }: SummaryTabProps): JSX.Element {
  const [summary, setSummary] = useState<SummaryData | null>(null);
  const [loading, setLoading] = useState<boolean>(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    loadSummary();
  }, [pagePath]);

  const loadSummary = async () => {
    setLoading(true);
    setError(null);

    try {
      // Convert page path to summary filename
      // Example: "01-Introducing-AI-Driven-Development/01-ai-development-revolution/01-moment_that_changed_everything"
      // -> "01-Introducing-AI-Driven-Development_01-moment_that_changed_everything.md"

      const pathParts = pagePath.split('/');
      const chapter = pathParts[0];
      const filename = pathParts[pathParts.length - 1];
      const summaryFilename = `${chapter}_${filename}.md`;

      // Fetch summary from summaries directory
      const summaryPath = `/summaries/${summaryFilename}`;

      const response = await fetch(summaryPath);

      if (!response.ok) {
        // Summary doesn't exist
        setSummary(null);
        setLoading(false);
        return;
      }

      const content = await response.text();
      const parsed = parseSummaryMarkdown(content);

      setSummary(parsed);
      setLoading(false);

    } catch (err) {
      console.error('Error loading summary:', err);
      setError('Failed to load summary');
      setLoading(false);
    }
  };

  const parseSummaryMarkdown = (content: string): SummaryData => {
    // Parse frontmatter and content
    const parts = content.split('---');

    if (parts.length < 3) {
      return {
        summary: content,
        keyConcepts: [],
        metadata: {
          chapter: '',
          difficulty: '',
          read_time: '',
          generated: ''
        }
      };
    }

    const frontmatter = parts[1];
    const body = parts[2];

    // Parse YAML frontmatter
    const metadata: any = {};
    frontmatter.split('\n').forEach(line => {
      const colonIndex = line.indexOf(':');
      if (colonIndex > 0) {
        const key = line.substring(0, colonIndex).trim();
        const value = line.substring(colonIndex + 1).trim();
        metadata[key] = value;
      }
    });

    // Extract summary text and key concepts
    let summaryText = '';
    const keyConcepts: string[] = [];

    const sections = body.split('##');
    sections.forEach(section => {
      const trimmed = section.trim();

      if (trimmed.startsWith('Summary')) {
        summaryText = trimmed.replace(/^Summary\s*/, '').trim();
      } else if (trimmed.startsWith('Key Concepts')) {
        const lines = trimmed.split('\n').slice(1); // Skip header
        lines.forEach(line => {
          const cleaned = line.trim();
          if (cleaned.startsWith('-')) {
            const concept = cleaned.substring(1).trim();
            if (concept) {
              keyConcepts.push(concept);
            }
          }
        });
      }
    });

    return {
      summary: summaryText,
      keyConcepts,
      metadata: {
        chapter: metadata.chapter || '',
        difficulty: metadata.difficulty || '',
        read_time: metadata.read_time || '',
        generated: metadata.generated || ''
      }
    };
  };

  if (loading) {
    return (
      <div className={styles.summaryContainer}>
        <div className={styles.loading}>
          <div className={styles.spinner}></div>
          <p>Loading summary...</p>
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div className={styles.summaryContainer}>
        <div className={styles.error}>
          <p>❌ {error}</p>
        </div>
      </div>
    );
  }

  if (!summary) {
    // Summary doesn't exist - show "Team Working on it"
    return (
      <div className={styles.summaryContainer}>
        <div className={styles.workingOnIt}>
          <div className={styles.workingIcon}>🔧</div>
          <h3>Team Working on it!</h3>
          <p>Our OLIVIA AI tutor is currently preparing a summary for this page.</p>
          <p className={styles.checkBack}>Check back soon!</p>
        </div>
      </div>
    );
  }

  // Summary exists - display it
  return (
    <div className={styles.summaryContainer}>
      {/* Metadata badges */}
      <div className={styles.metadata}>
        {summary.metadata.difficulty && (
          <span className={`${styles.badge} ${styles[`difficulty-${summary.metadata.difficulty}`]}`}>
            {summary.metadata.difficulty}
          </span>
        )}
        {summary.metadata.read_time && (
          <span className={styles.badge}>
            📖 {summary.metadata.read_time} min read
          </span>
        )}
      </div>

      {/* Summary content */}
      <div className={styles.summaryContent}>
        <h3>📝 Summary</h3>
        <p className={styles.summaryText}>{summary.summary}</p>
      </div>

      {/* Key concepts */}
      {summary.keyConcepts.length > 0 && (
        <div className={styles.keyConcepts}>
          <h4>💡 Key Concepts</h4>
          <ul>
            {summary.keyConcepts.map((concept, index) => (
              <li key={index}>{concept}</li>
            ))}
          </ul>
        </div>
      )}

      {/* Footer */}
      <div className={styles.footer}>
        <p className={styles.generatedBy}>
          ✨ Generated by OLIVIA AI Tutor
        </p>
      </div>
    </div>
  );
}
