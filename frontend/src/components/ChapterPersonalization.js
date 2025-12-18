import React, { useState, useEffect } from 'react';
import { useAuth } from '../contexts/AuthContext';
import { authClient } from '../auth/client';
import config from '../config';
import styles from './ChapterPersonalization.module.css';

const ChapterPersonalization = ({ chapterId, chapterTitle }) => {
  const { user } = useAuth();
  const [isPersonalized, setIsPersonalized] = useState(false);
  const [preferences, setPreferences] = useState({
    difficulty_level: 'default',
    focus_area: 'all',
    examples_preference: 'standard'
  });
  const [loading, setLoading] = useState(false);
  const [showPreferences, setShowPreferences] = useState(false);

  // Initialize default preferences based on user background
  useEffect(() => {
    if (user && !isPersonalized) {
      // Set default difficulty based on user's experience level
      let defaultDifficulty = 'default';
      if (user.experience_level) {
        if (user.experience_level.toLowerCase().includes('beginner')) {
          defaultDifficulty = 'beginner';
        } else if (user.experience_level.toLowerCase().includes('advanced')) {
          defaultDifficulty = 'advanced';
        } else if (user.experience_level.toLowerCase().includes('intermediate')) {
          defaultDifficulty = 'intermediate';
        }
      }

      // Set focus area based on user's background
      let defaultFocus = 'all';
      if (user.software_background && !user.hardware_background) {
        defaultFocus = 'code';
      } else if (!user.software_background && user.hardware_background) {
        defaultFocus = 'theory';
      } else if (user.software_background && user.hardware_background) {
        defaultFocus = 'all';
      }

      setPreferences({
        difficulty_level: defaultDifficulty,
        focus_area: defaultFocus,
        examples_preference: 'standard'
      });
    }
  }, [user]);

  // Load user preferences for this chapter if they exist
  useEffect(() => {
    if (user && chapterId) {
      fetchChapterPreferences();
    }
  }, [user, chapterId]);

  const fetchChapterPreferences = async () => {
    if (!user || !chapterId) return;

    try {
      // Use Better-Auth's session to get the token
      const session = await authClient.getSession();
      const token = session?.data?.session?.accessToken;

      if (!token) {
        console.error('No session token available');
        return;
      }

      const response = await fetch(`${config.API_BASE_URL}/user/chapter-preferences/${chapterId}`, {
        headers: {
          'Authorization': `Bearer ${token}`,
        },
      });

      if (response.ok) {
        const data = await response.json();
        if (data.preferences) {
          setPreferences(data.preferences);
          setIsPersonalized(true);
        }
      }
    } catch (error) {
      console.error('Error fetching chapter preferences:', error);
    }
  };

  const handlePreferenceChange = (key, value) => {
    setPreferences(prev => ({
      ...prev,
      [key]: value
    }));
  };

  const savePreferences = async () => {
    if (!user || !chapterId) return;

    setLoading(true);
    try {
      // Use Better-Auth's session to get the token
      const session = await authClient.getSession();
      const token = session?.data?.session?.accessToken;

      if (!token) {
        console.error('No session token available');
        return;
      }

      const response = await fetch(`${config.API_BASE_URL}/user/chapter-preferences/${chapterId}`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${token}`,
        },
        body: JSON.stringify({
          preferences: preferences
        }),
      });

      if (response.ok) {
        setIsPersonalized(true);
        setShowPreferences(false);
      } else {
        console.error('Failed to save preferences');
      }
    } catch (error) {
      console.error('Error saving preferences:', error);
    } finally {
      setLoading(false);
    }
  };

  const togglePersonalization = () => {
    if (isPersonalized) {
      // Reset to default preferences
      setPreferences({
        difficulty_level: 'default',
        focus_area: 'all',
        examples_preference: 'standard'
      });
      setIsPersonalized(false);
      setShowPreferences(false);
    } else {
      setShowPreferences(true);
    }
  };

  if (!user) {
    return (
      <div className={styles.personalizationContainer}>
        <p className={styles.loginPrompt}>Please <a href="/auth">sign in</a> to personalize this chapter.</p>
      </div>
    );
  }

  return (
    <div className={styles.personalizationContainer}>
      <div className={styles.personalizationHeader}>
        <h3>Personalize Content</h3>
        <button
          onClick={togglePersonalization}
          className={`${styles.personalizeButton} ${isPersonalized ? styles.active : ''}`}
        >
          {isPersonalized ? '✓ Personalized' : 'Personalize Content'}
        </button>
      </div>

      {showPreferences && (
        <div className={styles.preferencesForm}>
          <div className={styles.formGroup}>
            <label>Difficulty Level:</label>
            <select
              value={preferences.difficulty_level}
              onChange={(e) => handlePreferenceChange('difficulty_level', e.target.value)}
            >
              <option value="beginner">Beginner</option>
              <option value="intermediate">Intermediate</option>
              <option value="advanced">Advanced</option>
              <option value="default">Default</option>
            </select>
          </div>

          <div className={styles.formGroup}>
            <label>Focus Area:</label>
            <select
              value={preferences.focus_area}
              onChange={(e) => handlePreferenceChange('focus_area', e.target.value)}
            >
              <option value="all">All Topics</option>
              <option value="theory">Theory Focus</option>
              <option value="practice">Practice Focus</option>
              <option value="examples">Examples Focus</option>
              <option value="code">Code Focus</option>
            </select>
          </div>

          <div className={styles.formGroup}>
            <label>Examples Preference:</label>
            <select
              value={preferences.examples_preference}
              onChange={(e) => handlePreferenceChange('examples_preference', e.target.value)}
            >
              <option value="standard">Standard Examples</option>
              <option value="simple">Simple Examples</option>
              <option value="detailed">Detailed Examples</option>
              <option value="code-heavy">Code-Heavy Examples</option>
              <option value="visual">Visual Examples</option>
            </select>
          </div>

          <div className={styles.buttonGroup}>
            <button
              onClick={savePreferences}
              disabled={loading}
              className={styles.saveButton}
            >
              {loading ? 'Saving...' : 'Save Preferences'}
            </button>
            <button
              onClick={() => setShowPreferences(false)}
              className={styles.cancelButton}
            >
              Cancel
            </button>
          </div>
        </div>
      )}

      {isPersonalized && !showPreferences && (
        <div className={styles.currentPreferences}>
          <p><strong>Current Settings:</strong></p>
          <p>Difficulty: {preferences.difficulty_level}</p>
          <p>Focus: {preferences.focus_area}</p>
          <p>Examples: {preferences.examples_preference}</p>
          <button
            onClick={() => setShowPreferences(true)}
            className={styles.editButton}
          >
            Edit Preferences
          </button>
        </div>
      )}
    </div>
  );
};

export default ChapterPersonalization;