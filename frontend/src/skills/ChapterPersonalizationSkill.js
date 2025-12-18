import config from '../config';

class ChapterPersonalizationSkill {
  constructor() {
    this.name = 'chapter-personalization';
    this.description = 'Manage chapter personalization preferences for users';
  }

  async getChapterPreferences(chapterId, token) {
    try {
      const response = await fetch(`${config.API_BASE_URL}/user/chapter-preferences/${chapterId}`, {
        method: 'GET',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${token}`,
        },
      });

      if (!response.ok) {
        if (response.status === 404) {
          return null; // No preferences set yet
        }
        throw new Error(`Failed to fetch chapter preferences: ${response.status}`);
      }

      return await response.json();
    } catch (error) {
      console.error('Error fetching chapter preferences:', error);
      throw error;
    }
  }

  async setChapterPreferences(chapterId, preferences, token) {
    try {
      const response = await fetch(`${config.API_BASE_URL}/user/chapter-preferences/${chapterId}`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${token}`,
        },
        body: JSON.stringify({ preferences }),
      });

      if (!response.ok) {
        throw new Error(`Failed to set chapter preferences: ${response.status}`);
      }

      return await response.json();
    } catch (error) {
      console.error('Error setting chapter preferences:', error);
      throw error;
    }
  }

  async getPersonalizedContent(chapterId, userBackground, preferences) {
    // This would typically call an AI service to generate personalized content
    // For now, we'll return the original content with some basic personalization
    try {
      // Fetch original content
      const contentResponse = await fetch(`${config.API_BASE_URL}/textbook/chapters/${chapterId}`, {
        method: 'GET',
        headers: {
          'Content-Type': 'application/json',
        },
      });

      if (!contentResponse.ok) {
        throw new Error(`Failed to fetch chapter content: ${contentResponse.status}`);
      }

      const content = await contentResponse.json();

      // Apply basic personalization based on user background and preferences
      let personalizedContent = content.content;

      if (preferences && preferences.difficulty_level) {
        // This is where we would apply difficulty-based personalization
        // For now, just return the content with a note
        personalizedContent = `[[Personalized for difficulty: ${preferences.difficulty_level}]]\n\n${content.content}`;
      }

      if (preferences && preferences.focus_area && preferences.focus_area !== 'all') {
        // This is where we would apply focus area personalization
        personalizedContent = `[[Focus area: ${preferences.focus_area}]]\n\n${personalizedContent}`;
      }

      return {
        ...content,
        content: personalizedContent,
        personalized: true
      };
    } catch (error) {
      console.error('Error getting personalized content:', error);
      throw error;
    }
  }
}

export default ChapterPersonalizationSkill;