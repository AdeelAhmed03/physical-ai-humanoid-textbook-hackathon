import config from '../config';

class TranslationSkill {
  constructor() {
    this.name = 'translation';
    this.description = 'Translate content between languages';
    this.supportedLanguages = ['ur']; // Urdu
  }

  async translateText(text, targetLanguage = 'ur', token) {
    if (!this.supportedLanguages.includes(targetLanguage.toLowerCase())) {
      throw new Error(`Language ${targetLanguage} is not supported. Supported languages: ${this.supportedLanguages.join(', ')}`);
    }

    try {
      const response = await fetch(`${config.API_BASE_URL}/user/translate-chapter`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${token}`,
        },
        body: JSON.stringify({
          chapter_id: 'temp', // Not used for general text translation
          content: text,
          target_language: targetLanguage
        }),
      });

      if (!response.ok) {
        throw new Error(`Failed to translate text: ${response.status}`);
      }

      const result = await response.json();
      return result.translated_content;
    } catch (error) {
      console.error('Error translating text:', error);
      throw error;
    }
  }

  async translateChapterContent(chapterId, content, targetLanguage = 'ur', token) {
    if (!this.supportedLanguages.includes(targetLanguage.toLowerCase())) {
      throw new Error(`Language ${targetLanguage} is not supported. Supported languages: ${this.supportedLanguages.join(', ')}`);
    }

    try {
      const response = await fetch(`${config.API_BASE_URL}/user/translate-chapter`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${token}`,
        },
        body: JSON.stringify({
          chapter_id: chapterId,
          content: content,
          target_language: targetLanguage
        }),
      });

      if (!response.ok) {
        throw new Error(`Failed to translate chapter: ${response.status}`);
      }

      return await response.json();
    } catch (error) {
      console.error('Error translating chapter:', error);
      throw error;
    }
  }

  isLanguageSupported(language) {
    return this.supportedLanguages.includes(language.toLowerCase());
  }

  getSupportedLanguages() {
    return [...this.supportedLanguages];
  }
}

export default TranslationSkill;