import React, { useState, useEffect } from 'react';
import { useAuth } from '../contexts/AuthContext';
import config from '../config';
import styles from './ChapterTranslation.module.css';

const ChapterTranslation = ({ chapterId, chapterTitle, originalContent }) => {
  const { user, token } = useAuth();
  const [isTranslated, setIsTranslated] = useState(false);
  const [translatedContent, setTranslatedContent] = useState(null);
  const [loading, setLoading] = useState(false);
  const [translationError, setTranslationError] = useState(null);

  const translateContent = async () => {
    if (!user || !token || !chapterId || !originalContent) return;

    setLoading(true);
    setTranslationError(null);

    try {
      const response = await fetch(`${config.API_BASE_URL}/user/translate-chapter`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${token}`,
        },
        body: JSON.stringify({
          chapter_id: chapterId,
          content: originalContent,
          target_language: 'ur'
        }),
      });

      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.detail || 'Translation failed');
      }

      const data = await response.json();
      setTranslatedContent(data.translated_content);
      setIsTranslated(true);
    } catch (error) {
      console.error('Translation error:', error);
      setTranslationError(error.message);
    } finally {
      setLoading(false);
    }
  };

  const resetTranslation = () => {
    setIsTranslated(false);
    setTranslatedContent(null);
    setTranslationError(null);
  };

  if (!user) {
    return (
      <div className={styles.translationContainer}>
        <p className={styles.loginPrompt}>Please <a href="/auth">sign in</a> to translate this chapter to Urdu.</p>
      </div>
    );
  }

  return (
    <div className={styles.translationContainer}>
      <div className={styles.translationHeader}>
        <h3>Urdu Translation</h3>
        {!isTranslated ? (
          <button
            onClick={translateContent}
            disabled={loading}
            className={styles.translateButton}
          >
            {loading ? 'Translating...' : 'Translate to Urdu'}
          </button>
        ) : (
          <button
            onClick={resetTranslation}
            className={styles.resetButton}
          >
            Show Original
          </button>
        )}
      </div>

      {translationError && (
        <div className={styles.error}>
          <p>Translation Error: {translationError}</p>
          <button onClick={translateContent} className={styles.retryButton}>
            Retry Translation
          </button>
        </div>
      )}

      {isTranslated && translatedContent && (
        <div className={styles.translatedContent}>
          <div className={styles.translationNotice}>
            <strong>Urdu Translation:</strong>
          </div>
          <div
            className={styles.content}
            dir="rtl"
            lang="ur"
          >
            {translatedContent}
          </div>
        </div>
      )}
    </div>
  );
};

export default ChapterTranslation;