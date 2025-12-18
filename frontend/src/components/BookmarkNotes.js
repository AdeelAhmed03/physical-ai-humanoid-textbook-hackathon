import React, { useState, useEffect } from 'react';
import config from '@site/src/config';
import { useTheme } from '../contexts/ThemeContext';
import './BookmarkNotes.module.css';

const BookmarkNotes = ({ chapterId, contentBlockId, userId }) => {
  const [notes, setNotes] = useState('');
  const [bookmarks, setBookmarks] = useState([]);
  const [isBookmarked, setIsBookmarked] = useState(false);
  const { isDark } = useTheme();

  // Load existing notes and bookmarks when component mounts
  useEffect(() => {
    loadBookmarkAndNotes();
  }, [chapterId, contentBlockId, userId]);

  const loadBookmarkAndNotes = async () => {
    if (!userId || !chapterId) return;

    try {
      // Fetch user's bookmarks from the API
      const response = await fetch(`${config.API_BASE_URL}/user/bookmarks/${userId}`);
      if (response.ok) {
        const data = await response.json();
        setBookmarks(data.bookmarks);
        
        // Check if this specific content block is bookmarked
        const bookmarked = data.bookmarks.some(b => 
          b.chapter_id === parseInt(chapterId) && 
          b.content_block_id === parseInt(contentBlockId || 0)
        );
        setIsBookmarked(bookmarked);
        
        // Load existing notes if any
        const existingNote = data.bookmarks.find(b => 
          b.chapter_id === parseInt(chapterId) && 
          b.content_block_id === parseInt(contentBlockId || 0)
        );
        if (existingNote) {
          setNotes(existingNote.note || '');
        }
      }
    } catch (error) {
      console.error('Error loading bookmarks:', error);
    }
  };

  const handleSaveNotes = async () => {
    if (!userId || !chapterId) return;

    try {
      const bookmarkData = {
        user_id: userId,
        chapter_id: parseInt(chapterId),
        content_block_id: parseInt(contentBlockId || 0),
        note: notes
      };

      let response;
      if (isBookmarked) {
        // If already bookmarked, this would typically be an update
        // For now, we'll treat as a new creation since our API doesn't have update endpoint
        response = await fetch(`${config.API_BASE_URL}/user/bookmarks`, {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify(bookmarkData)
        });
      } else {
        response = await fetch(`${config.API_BASE_URL}/user/bookmarks`, {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify(bookmarkData)
        });
      }

      if (response.ok) {
        const newBookmark = await response.json();
        setBookmarks([...bookmarks, newBookmark]);
        setIsBookmarked(true);
        alert('Notes saved successfully!');
      } else {
        throw new Error('Failed to save notes');
      }
    } catch (error) {
      console.error('Error saving notes:', error);
      alert('Failed to save notes. Please try again.');
    }
  };

  const toggleBookmark = async () => {
    if (!userId || !chapterId) return;

    if (isBookmarked) {
      // If already bookmarked, we'd typically have an endpoint to remove
      // For now, just update the UI state
      setIsBookmarked(false);
      const updatedBookmarks = bookmarks.filter(b => 
        !(b.chapter_id === parseInt(chapterId) && 
          b.content_block_id === parseInt(contentBlockId || 0))
      );
      setBookmarks(updatedBookmarks);
    } else {
      // Create a bookmark with empty notes
      try {
        const bookmarkData = {
          user_id: userId,
          chapter_id: parseInt(chapterId),
          content_block_id: parseInt(contentBlockId || 0),
          note: notes
        };

        const response = await fetch(`${config.API_BASE_URL}/user/bookmarks`, {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify(bookmarkData)
        });

        if (response.ok) {
          const newBookmark = await response.json();
          setBookmarks([...bookmarks, newBookmark]);
          setIsBookmarked(true);
        } else {
          throw new Error('Failed to create bookmark');
        }
      } catch (error) {
        console.error('Error creating bookmark:', error);
        alert('Failed to create bookmark. Please try again.');
      }
    }
  };

  return (
    <div className={`bookmark-notes-container ${isDark ? 'dark-theme' : 'light-theme'}`}>
      <div className="bookmark-section">
        <button 
          className={`bookmark-button ${isBookmarked ? 'bookmarked' : ''}`}
          onClick={toggleBookmark}
          aria-label={isBookmarked ? "Remove bookmark" : "Bookmark this content"}
        >
          {isBookmarked ? '★' : '☆'}
        </button>
        <span className="bookmark-label">
          {isBookmarked ? 'Bookmarked' : 'Bookmark this content'}
        </span>
      </div>
      
      <div className="notes-section">
        <label htmlFor="notes-input">Add Notes:</label>
        <textarea
          id="notes-input"
          className="notes-input"
          value={notes}
          onChange={(e) => setNotes(e.target.value)}
          placeholder="Add your notes here..."
          rows="4"
        />
        <button 
          className="save-notes-button"
          onClick={handleSaveNotes}
        >
          Save Notes
        </button>
      </div>
    </div>
  );
};

export default BookmarkNotes;