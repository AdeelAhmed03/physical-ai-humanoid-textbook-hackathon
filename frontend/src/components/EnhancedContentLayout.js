import React from 'react';
import Layout from '@theme/Layout';
import { ThemeProvider, useTheme } from '../contexts/ThemeContext';
import ThemeToggle from '../components/ThemeToggle';
import ChatInterface from '../components/ChatInterface';
import BookmarkNotes from '../components/BookmarkNotes';
import ProgressTracker from '../components/ProgressTracker';
import './EnhancedContentLayout.module.css';

// Mock user ID - in a real app, this would come from auth
const MOCK_USER_ID = 1;

const EnhancedContentLayout = ({ children, title, description, currentChapter }) => {
  const { isDark } = useTheme();
  
  // Extract chapter ID from the slug or title
  const getChapterId = () => {
    if (currentChapter) {
      // Parse chapter ID from slug or other identifier
      return currentChapter.id || 1; // Default to 1 for demo
    }
    return 1; // Default chapter ID
  };

  const chapterId = getChapterId();

  return (
    <Layout title={title} description={description}>
      <div className={`enhanced-content-container ${isDark ? 'dark-theme' : 'light-theme'}`}>
        <header className="enhanced-content-header">
          <h1>{title}</h1>
          <div className="header-controls">
            <ThemeToggle />
          </div>
        </header>

        <div className="enhanced-content-main">
          <div className="content-area">
            <div className="content-body">
              {children}
              
              {/* Add bookmark and notes component */}
              <BookmarkNotes 
                chapterId={chapterId} 
                contentBlockId={1} // Would come from context in actual implementation  
                userId={MOCK_USER_ID} 
              />
              
              {/* Add progress tracker */}
              <ProgressTracker 
                chapterId={chapterId} 
                userId={MOCK_USER_ID} 
                title={title}
              />
            </div>
            
            {/* Add chat interface */}
            <div className="sidebar">
              <div className="chat-widget">
                <ChatInterface 
                  chapterId={chapterId} 
                  currentChapter={currentChapter} 
                />
              </div>
            </div>
          </div>
        </div>
      </div>
    </Layout>
  );
};

// Wrapper to ensure ThemeProvider is available
export default function EnhancedContentLayoutWrapper(props) {
  return (
    <ThemeProvider>
      <EnhancedContentLayout {...props} />
    </ThemeProvider>
  );
}