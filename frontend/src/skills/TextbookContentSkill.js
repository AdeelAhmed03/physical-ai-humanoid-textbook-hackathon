import config from '../config';

class TextbookContentSkill {
  constructor() {
    this.name = 'textbook-content';
    this.description = 'Retrieve and manage textbook content';
  }

  async getChapterContent(chapterId) {
    try {
      const response = await fetch(`${config.API_BASE_URL}/textbook/chapters/${chapterId}`, {
        method: 'GET',
        headers: {
          'Content-Type': 'application/json',
        },
      });

      if (!response.ok) {
        throw new Error(`Failed to fetch chapter content: ${response.status}`);
      }

      return await response.json();
    } catch (error) {
      console.error('Error fetching chapter content:', error);
      throw error;
    }
  }

  async searchContent(query, chapterId = null) {
    try {
      const params = new URLSearchParams({ query });
      if (chapterId) {
        params.append('chapter_id', chapterId);
      }

      const response = await fetch(`${config.API_BASE_URL}/search?${params}`, {
        method: 'GET',
        headers: {
          'Content-Type': 'application/json',
        },
      });

      if (!response.ok) {
        throw new Error(`Failed to search content: ${response.status}`);
      }

      return await response.json();
    } catch (error) {
      console.error('Error searching content:', error);
      throw error;
    }
  }

  async getTableOfContents() {
    try {
      const response = await fetch(`${config.API_BASE_URL}/textbook/toc`, {
        method: 'GET',
        headers: {
          'Content-Type': 'application/json',
        },
      });

      if (!response.ok) {
        throw new Error(`Failed to fetch table of contents: ${response.status}`);
      }

      return await response.json();
    } catch (error) {
      console.error('Error fetching table of contents:', error);
      throw error;
    }
  }
}

export default TextbookContentSkill;