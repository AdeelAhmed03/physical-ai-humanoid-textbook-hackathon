import React, { useState, useEffect } from 'react';
import { useLocation } from '@docusaurus/router';
import config from '../config';
import ChapterPersonalization from './ChapterPersonalization';
import ChapterTranslation from './ChapterTranslation';
import ClaudeCodeAgent from './ClaudeCodeAgent';
import { useAuth } from '../contexts/AuthContext';

const TextbookContent = ({ chapterId }) => {
  const [chapter, setChapter] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [displayContent, setDisplayContent] = useState('');
  const location = useLocation();
  const { user } = useAuth();

  useEffect(() => {
    // Extract chapter ID from URL if not provided as prop
    const extractChapterId = () => {
      const pathParts = location.pathname.split('/');
      if (pathParts.length >= 3 && pathParts[1] === 'docs') {
        return pathParts[2];
      }
      return chapterId || null;
    };

    const fetchChapter = async () => {
      try {
        setLoading(true);
        const id = extractChapterId();
        if (!id) {
          throw new Error('No chapter ID found');
        }

        const response = await fetch(`${config.API_BASE_URL}/textbook/${id}`);
        if (!response.ok) {
          throw new Error(`Failed to fetch chapter: ${response.status}`);
        }

        const data = await response.json();
        setChapter(data);
        setDisplayContent(data.content); // Set the original content initially
      } catch (err) {
        setError(err.message);
        console.error('Error fetching chapter:', err);
      } finally {
        setLoading(false);
      }
    };

    fetchChapter();
  }, [location.pathname, chapterId]);

  const handleContentUpdate = (newContent) => {
    setDisplayContent(newContent);
  };

  if (loading) {
    return <div>Loading chapter...</div>;
  }

  if (error) {
    return <div>Error loading chapter: {error}</div>;
  }

  if (!chapter) {
    return <div>No chapter found</div>;
  }

  // Render chapter content with new features
  return (
    <div>
      <h1>{chapter.title}</h1>

      {/* Claude Code Agent - available to all users */}
      <ClaudeCodeAgent chapterId={chapter.id || chapterId} currentContent={chapter.content} />

      {/* Personalization - only for logged in users */}
      {user && (
        <ChapterPersonalization
          chapterId={chapter.id || chapterId}
          chapterTitle={chapter.title}
        />
      )}

      {/* Translation - only for logged in users */}
      {user && config.ENABLE_URDU_TRANSLATION && (
        <ChapterTranslation
          chapterId={chapter.id || chapterId}
          chapterTitle={chapter.title}
          originalContent={chapter.content}
        />
      )}

      {/* Display content - either original or modified based on features */}
      <div
        dangerouslySetInnerHTML={{ __html: displayContent }}
      />
    </div>
  );
};

export default TextbookContent;