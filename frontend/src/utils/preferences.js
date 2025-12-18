// Utility functions for handling user preferences in the frontend
// Uses localStorage for client-side storage of preferences

export const preferencesUtils = {
  // Key for storing user preferences in localStorage
  PREFERENCES_KEY: 'ai-textbook-preferences',

  // Default preferences
  DEFAULT_PREFERENCES: {
    language: 'en',
    theme: 'light',
    fontSize: 'medium',
    learningPath: 'standard',
    completedChapters: []
  },

  // Get user preferences from localStorage
  getUserPreferences() {
    try {
      const prefs = localStorage.getItem(this.PREFERENCES_KEY);
      return prefs ? JSON.parse(prefs) : { ...this.DEFAULT_PREFERENCES };
    } catch (error) {
      console.warn('Error reading preferences from localStorage:', error);
      return { ...this.DEFAULT_PREFERENCES };
    }
  },

  // Save user preferences to localStorage
  setUserPreferences(preferences) {
    try {
      localStorage.setItem(this.PREFERENCES_KEY, JSON.stringify({
        ...this.DEFAULT_PREFERENCES,
        ...preferences
      }));
      return true;
    } catch (error) {
      console.error('Error saving preferences to localStorage:', error);
      return false;
    }
  },

  // Get specific preference value
  getPreference(key, defaultValue = null) {
    const prefs = this.getUserPreferences();
    return prefs[key] !== undefined ? prefs[key] : defaultValue;
  },

  // Set specific preference value
  setPreference(key, value) {
    const prefs = this.getUserPreferences();
    prefs[key] = value;
    return this.setUserPreferences(prefs);
  },

  // Update multiple preferences at once
  updatePreferences(updates) {
    const prefs = this.getUserPreferences();
    Object.assign(prefs, updates);
    return this.setUserPreferences(prefs);
  },

  // Reset to default preferences
  resetPreferences() {
    localStorage.removeItem(this.PREFERENCES_KEY);
  },

  // Track chapter completion
  markChapterCompleted(chapterId) {
    const prefs = this.getUserPreferences();
    if (!prefs.completedChapters.includes(chapterId)) {
      prefs.completedChapters.push(chapterId);
      this.setUserPreferences(prefs);
    }
  },

  // Check if a chapter is completed
  isChapterCompleted(chapterId) {
    const prefs = this.getUserPreferences();
    return prefs.completedChapters.includes(chapterId);
  }
};

// Export as default for easy import
export default preferencesUtils;